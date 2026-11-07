from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin,):
    list_display = (
        "created_at",
        "user",
        "action",
        "model_name",
        "object_id",
        "description",
    )

    list_filter = (
        "action",
        "model_name",
    )

    search_fields = ("description",)
