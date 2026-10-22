from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import StockDocument
from apps.catalog.models import Product

class WarehouseReportService:
    """Расчет бизнес-показателей складской программы."""

    @staticmethod
    def warehouse_kpi(days: int = 30) -> dict:
        """Расчет ключевых индикаторов эффективности склада."""
        since = timezone.now() - timedelta(days=days)
        executed_receipts = StockDocument.objects.filter(
            doc_type=StockDocument.DocType.RECEIPT,
            status=StockDocument.DocStatus.EXECUTED,
            created_at__gte=since,
        )
        total_turnover = executed_receipts.aggregate(total=Sum("total_cost"))["total"] or 0
        total_operations = StockDocument.objects.filter(created_at__gte=since, status=StockDocument.DocStatus.EXECUTED).count()

        return {
            "turnover_amount": float(total_turnover),
            "operations_count": total_operations,
            "avg_consignment_cost": float(total_turnover) / total_operations if total_operations else 0,
            "items_in_stock": Product.objects.filter(status=Product.StorageStatus.AVAILABLE).count(),
            "period_days": days,
        }

    @staticmethod
    def turnover_by_day(days: int = 30) -> list:
        since = timezone.now() - timedelta(days=days)
        rows = (
            StockDocument.objects.filter(
                status=StockDocument.DocStatus.EXECUTED,
                created_at__gte=since,
            )
            .extra(select={"day": "DATE(created_at)"})
            .values("day")
            .annotate(total=Sum("total_cost"))
            .order_by("day")
        )
        return [{"date": str(r["day"]), "total": float(r["total"])} for r in rows]

    @staticmethod
    def high_demand_products(limit: int = 5) -> list:
        """Топ ходовых товаров по частоте упоминания в складских накладных отгрузки."""
        rows = (
            StockDocument.objects.filter(
                doc_type=StockDocument.DocType.SHIPMENT,
                status=StockDocument.DocStatus.EXECUTED,
            )
            .values("product__category__name", "product__name")
            .annotate(count=Sum("quantity"))
            .order_by("-count")[:limit]
        )
        return [
            {"category": r["product__category__name"], "product": r["product__name"], "count": r["count"]}
            for r in rows
        ]

    @staticmethod
    def staff_load(days: int = 30) -> list:
        """Выработка складского персонала (обработано накладных)."""
        since = timezone.now() - timedelta(days=days)
        rows = (
            StockDocument.objects.filter(created_at__gte=since)
            .values("responsible_person__username")
            .annotate(count=Count("id"), volume=Sum("quantity"))
        )
        return [
            {"worker": r["responsible_person__username"], "documents": r["count"], "units_moved": r["volume"] or 0}
            for r in rows
        ]

    @staticmethod
    def current_stock_status() -> list:
        rows = Product.objects.values("status").annotate(count=Count("id"))
        return [{"status": r["status"], "count": r["count"]} for r in rows]
