# apps/customers/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]    
    filter_backends = [SearchFilter,]
    search_fields = ["name", "phone",]

    def get_queryset(self):
        return Customer.objects.filter(shop=self.request.user.shop)
    
    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop)
    
    @action(detail=True, methods=["get"])
    def statement(self, request, pk=None):
        customer = self.get_object()

        purchases = list(
            customer.purchases.values(
                "id",
                "purchase_date",
                "total_amount"
            )
        )

        payments = list(
            customer.payments.values(
                "id",
                "payment_date",
                "amount"
            )
        )

        return Response({
            "customer": customer.name,
            "total_purchases": customer.total_purchases,
            "total_payments": customer.total_payments,
            "balance": customer.balance,
            "purchases": purchases,
            "payments": payments
        })