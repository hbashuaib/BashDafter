# apps/purchases/serializers.py

from rest_framework import serializers

from apps.products.models import Product

from .models import Purchase, PurchaseItem


class PurchaseItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=False,
        allow_null=True,
    )

    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = PurchaseItem

        fields = (
            "id",
            "purchase",
            "product",
            "product_name",
            "item_name",
            "quantity",
            "unit_price",
            "total_price",
        )

        read_only_fields = ("total_price",)


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True, read_only=True,)
    customer_name = serializers.CharField(source="customer.name", read_only=True,)
    shop_name = serializers.CharField(source="customer.shop.name", read_only=True,)

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ("total_amount",)
