from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("kpi/", views.WarehouseKPIApiView.as_view(), name="warehouse_kpi"),
    path("turnover/", views.DailyTurnoverApiView.as_view(), name="turnover"),
    path("high-demand/", views.HighDemandProductsApiView.as_view(), name="high_demand"),
    path("staff-load/", views.StaffLoadApiView.as_view(), name="staff_load"),
    path("stock/", views.StockStatusApiView.as_view(), name="stock_status"),
]
