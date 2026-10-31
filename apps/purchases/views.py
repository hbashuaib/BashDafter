# apps/purchases/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Purchase, PurchaseItem
from .serializers import PurchaseSerializer, PurchaseItemSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(
            customer__shop=self.request.user.shop
        )


class PurchaseItemViewSet(viewsets.ModelViewSet):

    serializer_class = PurchaseItemSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return PurchaseItem.objects.filter(
            purchase__customer__shop=self.request.user.shop
        )