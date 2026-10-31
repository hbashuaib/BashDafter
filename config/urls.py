from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.customers.urls")),
    path("api/", include("apps.shops.urls")),
    path("api/", include("apps.purchases.urls")),
]