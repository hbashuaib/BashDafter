from django.contrib import admin

from .models import (
    InventoryTransaction,
    StockAdjustment,
)


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "adjustment_type",
        "quantity",
        "created_by",
        "created_at",
    )

    list_filter = ("adjustment_type",)

    search_fields = ("product__name",)

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "transaction_type",
        "quantity",
        "created_at",
    )

    list_filter = (
        "transaction_type",
    )

    search_fields = (
        "product__name",
    )