from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ProductViewSet,
    UnitViewSet,
)

router = DefaultRouter()

router.register(r"units", UnitViewSet,)
router.register(r"categories", CategoryViewSet,)
router.register(r"products", ProductViewSet,
)

urlpatterns = router.urls
