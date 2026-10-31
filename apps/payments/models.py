from django.db import models

from apps.customers.models import Customer


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.amount}"