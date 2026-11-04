from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import InventoryTransaction, StockAdjustment
from .serializers import (
    InventoryTransactionSerializer,
    StockAdjustmentSerializer,
)


class StockAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = StockAdjustment.objects.all().order_by("-created_at")
    serializer_class = StockAdjustmentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer,):
        serializer.save(
            created_by=self.request.user,
        )

class InventoryTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (InventoryTransaction.objects.all().order_by("-created_at"))
    serializer_class = InventoryTransactionSerializer