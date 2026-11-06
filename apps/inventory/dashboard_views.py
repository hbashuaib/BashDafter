from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product

from .models import (
    InventoryTransaction,
    StockAdjustment,
)


class InventoryDashboardView(APIView):
    def get(self, request):
        total_products = Product.objects.count()

        low_stock_products = Product.objects.filter(
            current_stock__lte=F("minimum_stock")
        ).count()

        stock_adjustments = StockAdjustment.objects.count()
        inventory_transactions = InventoryTransaction.objects.count()

        inventory_value = 0

        for product in Product.objects.all():
            inventory_value += product.current_stock * product.cost_price

        return Response(
            {
                "total_products": total_products,
                "low_stock_products": low_stock_products,
                "stock_adjustments": stock_adjustments,
                "inventory_transactions": inventory_transactions,
                "inventory_value": inventory_value,
            }
        )
