from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ChangePasswordView,
    HealthCheckView,
    UploadProfileImageView,
    UserProfileView,
)

urlpatterns = [
    path("health/", HealthCheckView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/profile/", UserProfileView.as_view(),),
    path("auth/profile/upload-image/", UploadProfileImageView.as_view(),),
    path("auth/change-password/", ChangePasswordView.as_view(),),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("", include("apps.accounts.user_urls"),),
]
