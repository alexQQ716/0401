from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "category", "category_name", "sku", "name", "price",
            "quantity_in_stock", "unit", "warehouse_cell", "status", "status_display",
            "description", "created_at"
        ]
        read_only_fields = ["created_at"]
