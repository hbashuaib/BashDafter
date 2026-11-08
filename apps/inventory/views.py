from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import (
    IsCashierOrAbove,
    IsManagerOrAbove,
    IsOwnerOrAdmin,
)
from apps.auditlog.utils import create_audit_log

from .models import InventoryTransaction, StockAdjustment
from .serializers import (
    InventoryTransactionSerializer,
    StockAdjustmentSerializer,
)


class StockAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = StockAdjustment.objects.all().order_by("-created_at")
    serializer_class = StockAdjustmentSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return (
            StockAdjustment.objects
            .filter(
                product__shop=self.request.user.shop,
            )
            .order_by(
                "-created_at"
            )
        )
    
    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
        ]:
            permission_classes = [IsCashierOrAbove,]

        elif self.action in [
            "create",
            "update",
            "partial_update",
        ]:
            permission_classes = [IsManagerOrAbove,]

        elif self.action == "destroy":
            permission_classes = [IsOwnerOrAdmin,]

        else:
            permission_classes = [IsAuthenticated,]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer,):
        adjustment = serializer.save(created_by=self.request.user,)

        create_audit_log(
            user=self.request.user,
            action="CREATE",
            model_name="StockAdjustment",
            object_id=adjustment.id,
            description=(
                f"Created "
                f"{adjustment.adjustment_type} "
                f"adjustment for "
                f"{adjustment.product.name}"
            ),
        )
        
    def perform_update(self, serializer,):
        adjustment = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="UPDATE",
            model_name="StockAdjustment",
            object_id=adjustment.id,
            description=(
                f"Updated "
                f"{adjustment.adjustment_type} "
                f"adjustment for "
                f"{adjustment.product.name}"
            ),
        )

class InventoryTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = (InventoryTransactionSerializer)
    permission_classes = (IsCashierOrAbove,)

    def get_queryset(self,):
        return (
            InventoryTransaction.objects
            .filter(
                product__shop=self.request.user.shop,
            )
            .order_by(
                "-created_at"
            )
        )