from rest_framework.views import APIView
from rest_framework.response import Response
from .services import WarehouseReportService

class WarehouseKPIApiView(APIView):
    def get(self, request):
        days = int(request.query_params.get("days", 30))
        return Response(WarehouseReportService.warehouse_kpi(days))

class DailyTurnoverApiView(APIView):
    def get(self, request):
        days = int(request.query_params.get("days", 30))
        return Response(WarehouseReportService.turnover_by_day(days))

class HighDemandProductsApiView(APIView):
    def get(self, request):
        limit = int(request.query_params.get("limit", 5))
        return Response(WarehouseReportService.high_demand_products(limit))

class StaffLoadApiView(APIView):
    def get(self, request):
        days = int(request.query_params.get("days", 30))
        return Response(WarehouseReportService.staff_load(days))

class StockStatusApiView(APIView):
    def get(self, request):
        return Response(WarehouseReportService.current_stock_status())
