from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "amount",
        "payment_date",
    )

    search_fields = (
        "customer__name",
    )