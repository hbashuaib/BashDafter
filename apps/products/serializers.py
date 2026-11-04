from django.db import models
from rest_framework import serializers

from apps.purchases.models import PurchaseItem

from .models import (
    Category,
    Product,
    Unit,
)


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True,)
    unit_name = serializers.CharField(source="unit.name", read_only=True,)
    is_low_stock = serializers.BooleanField(read_only=True,)
    total_sold = serializers.SerializerMethodField()
    total_adjustments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        
    def get_total_sold(self, obj):
        return (
            PurchaseItem.objects
            .filter(product=obj)
            .aggregate(
                total=models.Sum("quantity")
            )["total"]
            or 0
        )
        
    def get_total_adjustments(self, obj,):
        return (
            obj.stock_adjustments.count()
        )
