from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.catalog.models import Product
from apps.clients.models import Counterparty

class StockDocument(models.Model):
    """Складской ордер движения материальных ценностей."""
    
    class DocType(models.TextChoices):
        RECEIPT = "receipt", "Приход (Поступление ТМЦ)"
        SHIPMENT = "shipment", "Расход (Отгрузка со склада)"
        WRITE_OFF = "write_off", "Списание (Убыль/Порча)"

    class DocStatus(models.TextChoices):
        DRAFT = "draft", "Черновик (Создан)"
        CONFIRMED = "confirmed", "Проверен кладовщиком"
        EXECUTED = "executed", "Проведен по складу"
        CANCELLED = "cancelled", "Аннулирован"

    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE, related_name="documents", verbose_name="Контрагент")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="documents", verbose_name="Товар")
    responsible_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="documents", verbose_name="Ответственный")
    doc_type = models.CharField("Тип складской операции", max_length=20, choices=DocType.choices)
    quantity = models.PositiveIntegerField("Количество товара", default=1)
    total_cost = models.DecimalField("Общая стоимость партии, ₽", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("Статус документа", max_length=20, choices=DocStatus.choices, default=DocStatus.DRAFT)
    comment = models.TextField("Служебные отметки / Комментарий", blank=True)
    created_at = models.DateTimeField("Дата составления", auto_now_add=True)
    executed_at = models.DateTimeField("Дата проведения по балансу", null=True, blank=True)

    class Meta:
        verbose_name = "Складской документ"
        verbose_name_plural = "Складские документы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Ордер №{self.pk} ({self.get_doc_type_display()})"

    def save(self, *args, **kwargs):
        # Каскадная логика: резервирование товара при фиксации Отгрузки (Shipment)
        if not self.pk and self.doc_type == self.DocType.SHIPMENT:
            if self.product.quantity_in_stock >= self.quantity:
                self.product.status = Product.StorageStatus.RESERVED
                self.product.save()
        super().save(*args, **kwargs)

    def execute_document(self):
        """Проведение накладной с каскадным пересчётом физических остатков."""
        self.status = self.DocStatus.EXECUTED
        self.executed_at = timezone.now()
        
        if self.doc_type == self.DocType.RECEIPT:
            self.product.quantity_in_stock += self.quantity
            self.product.status = Product.StorageStatus.AVAILABLE
        elif self.doc_type in [self.DocType.SHIPMENT, self.DocType.WRITE_OFF]:
            if self.product.quantity_in_stock >= self.quantity:
                self.product.quantity_in_stock -= self.quantity
                if self.product.quantity_in_stock == 0:
                    self.product.status = Product.StorageStatus.OUT_OF_STOCK
                else:
                    self.product.status = Product.StorageStatus.AVAILABLE
            else:
                raise ValueError("Недостаточно товара на складе для проведения списания/отгрузки!")
                
        self.product.save()
        self.save()

    def cancel_document(self):
        """Аннулирование операции."""
        self.status = self.DocStatus.CANCELLED
        if self.doc_type == self.DocType.SHIPMENT and self.product.status == Product.StorageStatus.RESERVED:
            self.product.status = Product.StorageStatus.AVAILABLE
            self.product.save()
        self.save()
