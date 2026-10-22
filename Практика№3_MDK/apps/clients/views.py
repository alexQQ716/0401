from rest_framework import viewsets, filters
from .models import Counterparty
from .serializers import CounterpartySerializer

class CounterpartyViewSet(viewsets.ModelViewSet):
    queryset = Counterparty.objects.select_related("manager").all()
    serializer_class = CounterpartySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["company_name", "inn", "phone"]
    ordering_fields = ["created_at", "company_name"]
