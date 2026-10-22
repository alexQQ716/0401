from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Регистрация маршрутов всех 5 подсистем программы
    path("api/auth/", include("apps.accounts.urls")),
    path("api/", include("apps.catalog.urls")),
    path("api/clients/", include("apps.clients.urls")),
    path("api/documents/", include("apps.orders.urls")),
    path("api/analytics/", include("apps.reports.urls")),
    path("api/drf-login/", include("rest_framework.urls")),
]

