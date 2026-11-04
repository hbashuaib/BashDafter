from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product


class TopSellingProductsView(APIView):
    def get(self, request):

        products = (
            Product.objects.filter(
                purchase_items__isnull=False,
            )
            .annotate(total_sold=Sum("purchase_items__quantity"))
            .order_by("-total_sold")[:10]
        )

        data = []

        for product in products:
            data.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "total_sold": product.total_sold,
                    "current_stock": product.current_stock,
                }
            )

        return Response(data)
