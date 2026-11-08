# apps/purchases/views.py

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import (
    IsCashierOrAbove,
    IsManagerOrAbove,
    IsOwnerOrAdmin,
)
from apps.auditlog.utils import create_audit_log

from .models import Purchase, PurchaseItem
from .serializers import PurchaseItemSerializer, PurchaseSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer    

    def get_queryset(self):
        return Purchase.objects.filter(customer__shop=self.request.user.shop)
    
    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
            "create",
        ]:
            permission_classes = [IsCashierOrAbove,]

        elif self.action in [
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
        purchase = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="CREATE",
            model_name="Purchase",
            object_id=purchase.id,
            description=(
                f"Created purchase "
                f"#{purchase.id}"
            ),
        )
    
    def perform_update(self, serializer,):
        purchase = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="UPDATE",
            model_name="Purchase",
            object_id=purchase.id,
            description=(
                f"Updated purchase "
                f"#{purchase.id}"
            ),
        )
    
    def destroy(self, request, *args, **kwargs,):
        raise ValidationError(
            "Deleting purchases is not allowed."
        )
    

class PurchaseItemViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PurchaseItem.objects.filter(
            purchase__customer__shop=self.request.user.shop
        )
    
    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
            "create",
        ]:
            permission_classes = [IsCashierOrAbove,]

        elif self.action in [
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
        item = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="CREATE",
            model_name="PurchaseItem",
            object_id=item.id,
            description=(
                f"Added item "
                f"{item.item_name} "
                f"to purchase "
                f"#{item.purchase.id}"
            ),
        )
        
    def perform_update(self, serializer,):
        item = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="UPDATE",
            model_name="PurchaseItem",
            object_id=item.id,
            description=(
                f"Updated item "
                f"{item.item_name} "
                f"in purchase "
                f"#{item.purchase.id}"
            ),
        )
        
    def destroy(self, request, *args, **kwargs,):
        raise ValidationError(
            "Deleting purchase items is not allowed."
        )
