from rest_framework import viewsets, decorators, status
from rest_framework.response import Response
from .models import StockDocument
from .serializers import StockDocumentSerializer

class StockDocumentViewSet(viewsets.ModelViewSet):
    queryset = StockDocument.objects.select_related("counterparty", "product", "responsible_person").all()
    serializer_class = StockDocumentSerializer

    def perform_create(self, serializer):
        serializer.save(responsible_person=self.request.user)

    @decorators.action(detail=True, methods=["post"])
    def execute(self, request, pk=None):
        doc = self.get_object()
        try:
            doc.execute_document()
            return Response({"status": "Документ успешно проведен, баланс остатков изменен"})
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        doc = self.get_object()
        doc.cancel_document()
        return Response({"status": "Документ аннулирован"})

