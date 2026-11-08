from rest_framework import viewsets
from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import (
    IsCashierOrAbove,
    IsManagerOrAbove,
    IsOwnerOrAdmin,
)
from apps.auditlog.utils import create_audit_log

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Payment.objects.filter(
            customer__shop=self.request.user.shop
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
        customer = serializer.validated_data["customer"]

        if (
            customer.shop
            != self.request.user.shop
        ):
            raise PermissionDenied(
                "Customer does not belong to your shop."
            )

        payment = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="CREATE",
            model_name="Payment",
            object_id=payment.id,
            description=(
                f"Created payment "
                f"{payment.amount} "
                f"for "
                f"{payment.customer.name}"
            ),
        )
        
    def perform_update(self, serializer,):
        payment = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="UPDATE",
            model_name="Payment",
            object_id=payment.id,
            description=(
                f"Updated payment "
                f"#{payment.id}"
            ),
        )
    
    def destroy(self, request, *args, **kwargs,):
            raise ValidationError(
                "Deleting purchases is not allowed."
            )