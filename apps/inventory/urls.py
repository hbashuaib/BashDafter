from rest_framework.routers import DefaultRouter

from .views import InventoryTransactionViewSet, StockAdjustmentViewSet

router = DefaultRouter()

router.register(r"stock-adjustments", StockAdjustmentViewSet, basename="stock-adjustments",)
router.register(r"inventory-transactions", InventoryTransactionViewSet, basename="inventory-transactions",)

urlpatterns = router.urls
