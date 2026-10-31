from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(
            customer__shop=self.request.user.shop
        )

def perform_create(self, serializer):

    customer = serializer.validated_data["customer"]

    if customer.shop != self.request.user.shop:
        raise PermissionDenied(
            "Customer does not belong to your shop."
        )

    serializer.save()