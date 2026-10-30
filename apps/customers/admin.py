from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "shop",
        "phone",
        "current_balance",
        "is_active",
    )

    search_fields = (
        "name",
        "phone",
    )

    list_filter = (
        "shop",
        "is_active",
    )
    
    def current_balance(self, obj):
        return obj.balance


    current_balance.short_description = "Balance"