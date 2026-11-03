from rest_framework import viewsets

from .models import (
    Category,
    Product,
    Unit,
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    UnitSerializer,
)


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
