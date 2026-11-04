from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from apps.customers.models import Customer
from apps.inventory.models import InventoryTransaction


class Purchase(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="purchases"
    )
    purchase_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total(self):
        total = self.items.aggregate(total=Sum("total_price"))["total"] or 0
        self.total_amount = total
        self.save(update_fields=["total_amount"])

    def __str__(self):
        return f"{self.customer.name} - {self.purchase_date}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="purchase_items",
        null=True,
        blank=True,
    )
    item_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

        if is_new and self.product:
            if self.product.current_stock < self.quantity:
                raise ValidationError(
                    f"Not enough stock available for "
                    f"{self.product.name}."
                )

            self.product.current_stock -= self.quantity
            
            InventoryTransaction.objects.create(
                product=self.product,
                transaction_type="SALE",
                quantity=self.quantity,
                reference=f"Sale #{self.purchase.id}",
            )

            self.product.save(
                update_fields=[
                    "current_stock",
                ]
            )

        self.purchase.update_total()

    def delete(self, *args, **kwargs):
        purchase = self.purchase

        if self.product:
            self.product.current_stock += self.quantity            

            self.product.save(
                update_fields=[
                    "current_stock",
                ]
            )

        super().delete(*args, **kwargs)

        purchase.update_total()

    def __str__(self):
        return self.item_name
