from rest_framework import serializers
from .models import StockDocument

class StockDocumentSerializer(serializers.ModelSerializer):
    counterparty_name = serializers.CharField(source="counterparty.company_name", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    responsible_name = serializers.CharField(source="responsible_person.get_full_name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    doc_type_display = serializers.CharField(source="get_doc_type_display", read_only=True)

    class Meta:
        model = StockDocument
        fields = [
            "id", "counterparty", "counterparty_name", "product", "product_name",
            "responsible_person", "responsible_name", "doc_type", "doc_type_display",
            "quantity", "total_cost", "status", "status_display",
            "comment", "created_at", "executed_at"
        ]
        read_only_fields = ["responsible_person", "created_at", "executed_at"]
