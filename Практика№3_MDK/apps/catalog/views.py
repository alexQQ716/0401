from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

class ProductViewSet(viewsets.ModelViewSet):
    """Эндпоинты для управления остатками товаров."""
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "status", "warehouse_cell"]
    search_fields = ["name", "sku", "warehouse_cell"]
    ordering_fields = ["price", "quantity_in_stock", "created_at"]
