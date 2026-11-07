from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import (
    IsCashierOrAbove,
    IsManagerOrAbove,
    IsOwnerOrAdmin,
)
from apps.auditlog.utils import create_audit_log

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

    def get_queryset(self):
        return Product.objects.filter(
            shop=self.request.user.shop,
            is_active=True,
        )

    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
        ]:
            permission_classes = [IsCashierOrAbove,]

        elif self.action in [
            "create",
            "update",
            "partial_update",
        ]:
            permission_classes = [IsManagerOrAbove,]

        elif self.action in [
            "destroy",
            "restore",
            "inactive",
        ]:
            permission_classes = [IsOwnerOrAdmin,]

        else:
            permission_classes = [IsAuthenticated,]

        return [
            permission()
            for permission in permission_classes
        ]
        
    def perform_create(self, serializer,):
        product = serializer.save(shop=self.request.user.shop,)

        create_audit_log(
            user=self.request.user,
            action="CREATE",
            model_name="Product",
            object_id=product.id,
            description=(
                f"Created product {product.name}"
            ),
        )
        
    def perform_update(self, serializer,):
        product = serializer.save()

        create_audit_log(
            user=self.request.user,
            action="UPDATE",
            model_name="Product",
            object_id=product.id,
            description=(
                f"Updated product {product.name}"
            ),
        )
        
    def perform_destroy(self, instance,):
        product_name = instance.name
        product_id = instance.id

        instance.is_active = False
        instance.save()

        create_audit_log(
            user=self.request.user,
            action="DELETE",
            model_name="Product",
            object_id=product_id,
            description=(
                f"Deactivated product "
                f"{product_name}"
            ),
        )
        
    @action(detail=False, methods=["get"],)
    def inactive(self, request,):
        products = Product.objects.filter(
            shop=request.user.shop,
            is_active=False,
        )

        serializer = self.get_serializer(products, many=True,)
        
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"],)
    def restore(self, request, pk=None,):
        product = get_object_or_404(
            Product,
            pk=pk,
            shop=request.user.shop,
            is_active=False,
        )

        product.is_active = True
        product.save()

        create_audit_log(
            user=request.user,
            action="RESTORE",
            model_name="Product",
            object_id=product.id,
            description=(
                f"Restored product "
                f"{product.name}"
            ),
        )

        return Response(
            {
                "message":
                    "Product restored successfully"
            }
        )
