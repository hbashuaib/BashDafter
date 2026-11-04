from rest_framework import serializers

from .models import InventoryTransaction, StockAdjustment


class StockAdjustmentSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True,)

    class Meta:
        model = StockAdjustment
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "created_at",
        )

class InventoryTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True,)

    class Meta:
        model = InventoryTransaction
        fields = "__all__"