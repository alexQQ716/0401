from rest_framework import serializers
from .models import Counterparty

class CounterpartySerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source="manager.get_full_name", read_only=True)

    class Meta:
        model = Counterparty
        fields = ["id", "company_name", "inn", "phone", "email", "contract_number", "manager", "manager_name", "created_at"]
        read_only_fields = ["created_at"]

    def validate_phone(self, value):
        qs = Counterparty.objects.filter(phone=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Контрагент с таким телефоном уже зарегистрирован")
        return value
