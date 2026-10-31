from django.db import models
from django.db.models import Sum

from apps.shops.models import Shop


class Customer(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="customers")
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_purchases(self):
        result = self.purchases.aggregate(total=Sum("total_amount"))

        return result["total"] or 0
    
    @property
    def total_payments(self):
        result = self.payments.aggregate(total=Sum("amount"))

        return result["total"] or 0
    
    @property
    def balance(self):
        return self.total_purchases - self.total_payments
    
    @property
    def current_statement(self):
        return {
            "customer": self.name,
            "purchases": self.total_purchases,
            "payments": self.total_payments,
            "balance": self.balance,
        }

    def __str__(self):
        return self.name