# apps/purchases/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Purchase
from .serializers import PurchaseSerializer


class PurchaseViewSet(viewsets.ModelViewSet):

    serializer_class = PurchaseSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Purchase.objects.filter(
            customer__shop=self.request.user.shop
        )