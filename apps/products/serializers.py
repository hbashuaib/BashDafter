from django.db import models
from rest_framework import serializers

from apps.purchases.models import PurchaseItem

from .models import (
    Category,
    Product,
    Unit,
)


class UnitSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = "__all__"

    def get_display_name(self, obj):
        return (
            obj.name_en
            or obj.name_ar
            or obj.name
        )


class CategorySerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_display_name(self, obj):
        return (
            obj.name_en
            or obj.name_ar
            or obj.name
        )



class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True,)
    unit_name = serializers.CharField(source="unit.name", read_only=True,)
    is_low_stock = serializers.BooleanField(read_only=True,)
    total_sold = serializers.SerializerMethodField()
    total_adjustments = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("shop",)
        
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
    
    def get_display_name(self, obj):
        return (
            obj.name_en
            or obj.name_ar
            or obj.name
        )
