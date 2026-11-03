# apps/purchases/urls.py

from rest_framework.routers import DefaultRouter

from .views import PurchaseItemViewSet, PurchaseViewSet

router = DefaultRouter()

router.register(r"purchases", PurchaseViewSet, basename="purchases")
router.register(r"purchase-items", PurchaseItemViewSet, basename="purchase-items")

urlpatterns = router.urls
