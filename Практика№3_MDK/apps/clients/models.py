from django.db import models
from django.conf import settings

class Counterparty(models.Model):
    """Юридические и физические лица (Поставщики, Покупатели, Смежники)."""
    
    company_name = models.CharField("Название организации / ФИО", max_length=150)
    inn = models.CharField("ИНН организации", max_length=12, unique=True)
    phone = models.CharField("Контактный телефон", max_length=20, unique=True)
    email = models.EmailField("Электронная почта", blank=True)
    contract_number = models.CharField("Договор сотрудничества", max_length=50)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="counterparties", verbose_name="Закрепленный менеджер"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.company_name} (ИНН: {self.inn})"
