from datetime import timedelta

from django.db.models import F
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product

from .models import (
    InventoryTransaction,
    StockAdjustment,
)


class InventoryDashboardView(APIView):
    def get(self, request):
        shop = request.user.shop
        total_products = Product.objects.filter(
            shop=shop,
            is_active=True,
        ).count()

        low_stock_products = Product.objects.filter(
            shop=shop,
            is_active=True,
            current_stock__lte=F("minimum_stock"),
        ).count()

        expiring_products = Product.objects.filter(
            shop=shop,
            is_active=True,
            has_expiry=True,
            expiry_date__isnull=False,
            expiry_date__lte=(timezone.now().date() + timedelta(days=30)),
        ).count()

        stock_adjustments = StockAdjustment.objects.filter(
            product__shop=shop,
        ).count()

        inventory_transactions = InventoryTransaction.objects.filter(
            product__shop=shop,
        ).count()

        inventory_value = 0

        for product in Product.objects.filter(
            shop=shop,
            is_active=True,
        ):
            inventory_value += product.current_stock * product.cost_price

        return Response(
            {
                "total_products": total_products,
                "low_stock_products": low_stock_products,
                "expiring_products": expiring_products,
                "stock_adjustments": stock_adjustments,
                "inventory_transactions": inventory_transactions,
                "inventory_value": inventory_value,
            }
        )
