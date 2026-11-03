from django.contrib import admin

from .models import (
    Category,
    Product,
    Unit,
)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "unit",
        "selling_price",
        "is_active",
    )

    list_filter = (
        "is_active",
        "category",
        "unit",
    )

    search_fields = (
        "name",
        "barcode",
    )
