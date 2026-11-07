from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "BashDafter Information",
            {
                "fields": (
                    "shop",
                    "role",
                    "phone_number",
                    "profile_image",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "shop",
        "role",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_active",
    )