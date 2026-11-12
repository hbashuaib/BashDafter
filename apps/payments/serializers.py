# apps/payments/serializers.py

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True,)
    shop_name = serializers.CharField(source="customer.shop.name", read_only=True,)

    class Meta:
        model = Payment
        fields = "__all__"