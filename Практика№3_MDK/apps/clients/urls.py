from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CounterpartyViewSet

router = DefaultRouter()
router.register("", CounterpartyViewSet, basename="counterparties")

urlpatterns = [
    path("", include(router.urls)),
]
