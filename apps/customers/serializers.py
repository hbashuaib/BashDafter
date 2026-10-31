# apps/customers/serializers.py

from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    balance = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = "__all__"