from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockDocumentViewSet

router = DefaultRouter()
router.register("", StockDocumentViewSet, basename="documents")

urlpatterns = [
    path("", include(router.urls)),
]
