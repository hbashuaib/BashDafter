from rest_framework.routers import DefaultRouter

from .dashboard_views import InventoryDashboardView
from .top_selling_views import TopSellingProductsView
from .views import InventoryTransactionViewSet, StockAdjustmentViewSet

router = DefaultRouter()

router.register(r"stock-adjustments", StockAdjustmentViewSet, basename="stock-adjustments",)
router.register(r"inventory-transactions", InventoryTransactionViewSet, basename="inventory-transactions",)

from django.urls import path

urlpatterns = [
    path("inventory-dashboard/", InventoryDashboardView.as_view(),),
    path("top-selling-products/", TopSellingProductsView.as_view(),),
]

urlpatterns += router.urls

