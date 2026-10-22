from django.db import models

class Category(models.Model):
    """Категории и группы ТМЦ (например, Строительные материалы, Инструменты)."""
    name = models.CharField("Название категории", max_length=50, unique=True)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    """Учётная карточка товара на складе."""
    
    class StorageStatus(models.TextChoices):
        AVAILABLE = "available", "В наличии"
        RESERVED = "reserved", "Забронирован под отгрузку"
        OUT_OF_STOCK = "out_of_stock", "Отсутствует"

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="Категория")
    sku = models.CharField("Артикул / Штрихкод", max_length=50, unique=True)
    name = models.CharField("Наименование товара", max_length=150)
    price = models.DecimalField("Закупочная стоимость, ₽", max_digits=12, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField("Остаток на складе", default=0)
    unit = models.CharField("Ед. измерения", max_length=10, default="шт.")
    warehouse_cell = models.CharField("Адрес хранения (Зона/Ячейка)", max_length=30, blank=True)
    status = models.CharField("Статус остатка", max_length=20, choices=StorageStatus.choices, default=StorageStatus.AVAILABLE)
    description = models.TextField("Характеристики / Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар на складе"
        verbose_name_plural = "Товары на складе"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.sku}] {self.name}"
