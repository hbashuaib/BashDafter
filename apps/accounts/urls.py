from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import HealthCheckView, UserProfileView

urlpatterns = [
    path("health/", HealthCheckView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/profile/", UserProfileView.as_view(),),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
