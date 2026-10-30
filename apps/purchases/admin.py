from django.contrib import admin

from .models import Purchase
from .models import PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "purchase_date",
        "total_amount",
    )

    inlines = [
        PurchaseItemInline,
    ]