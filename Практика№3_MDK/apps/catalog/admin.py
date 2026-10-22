from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "price", "quantity_in_stock", "warehouse_cell", "status")
    list_editable = ("status", "warehouse_cell", "quantity_in_stock")
    search_fields = ("sku", "name")
