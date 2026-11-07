# apps/customers/views.py

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import (
    IsCashierOrAbove,
    IsManagerOrAbove,
    IsOwnerOrAdmin,
)
from apps.auditlog.utils import create_audit_log

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = (
        "name",
        "phone",
    )

    def get_queryset(self):
        return Customer.objects.filter(
            shop=self.request.user.shop,
            is_active=True,
        )

    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
            "statement",
            "stats",
        ]:
            permission_classes = [
                IsCashierOrAbove,
            ]

        elif self.action in [
            "create",
            "update",
            "partial_update",
        ]:
            permission_classes = [
                IsManagerOrAbove,
            ]

        elif self.action in [
            "destroy",
            "restore",
            "inactive",
        ]:
            permission_classes = [
                IsOwnerOrAdmin,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
            ]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer,):
        customer = serializer.save(shop=self.request.user.shop,)

        create_audit_log(
            user=self.request.user,
            action="CREATE",
            model_name="Customer",
            object_id=customer.id,
            description=(f"Created customer {customer.name}"),
        )

    def perform_update(self, serializer,):
        customer = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="UPDATE",
            model_name="Customer",
            object_id=customer.id,
            description=(f"Updated customer {customer.name}"),
        )

    def perform_destroy(self, instance,):
        customer_name = instance.name
        customer_id = instance.id

        instance.is_active = False
        instance.save()

        create_audit_log(
            user=self.request.user,
            action="DELETE",
            model_name="Customer",
            object_id=customer_id,
            description=(f"Deactivated customer {customer_name}"),
        )
        
    @action(detail=False, methods=["get"],)
    def inactive(self, request,):
        customers = Customer.objects.filter(
            shop=request.user.shop,
            is_active=False,
        )

        serializer = self.get_serializer(
            customers,
            many=True,
        )

        return Response(serializer.data)
        

    @action(detail=True, methods=["post"],)
    def restore(self, request, pk=None,):
        customer = get_object_or_404(
            Customer,
            pk=pk,
            shop=request.user.shop,
            is_active=False,
        )
        customer.is_active = True
        customer.save()

        create_audit_log(
            user=request.user,
            action="RESTORE",
            model_name="Customer",
            object_id=customer.id,
            description=(f"Restored customer {customer.name}"),
        )

        return Response({"message": "Customer restored successfully"})

    @action(detail=True, methods=["get"])
    def statement(self, request, pk=None):
        customer = self.get_object()

        purchases = list(
            customer.purchases.values("id", "purchase_date", "total_amount")
        )

        payments = list(customer.payments.values("id", "payment_date", "amount"))

        return Response(
            {
                "customer": customer.name,
                "total_purchases": customer.total_purchases,
                "total_payments": customer.total_payments,
                "balance": customer.balance,
                "purchases": purchases,
                "payments": payments,
            }
        )

    @action(detail=True, methods=["get"])
    def stats(self, request, pk=None):
        customer = self.get_object()

        return Response(
            {
                "customer": customer.name,
                "purchase_count": customer.purchases.count(),
                "payment_count": customer.payments.count(),
                "total_purchases": customer.total_purchases,
                "total_payments": customer.total_payments,
                "balance": customer.balance,
            }
        )
