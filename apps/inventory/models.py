from django.db import models


class StockAdjustment(models.Model):
    ADJUSTMENT_TYPES = (
        ("OPENING", "Opening Stock"),
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
        ("DAMAGE", "Damaged Stock"),
        ("CORRECTION", "Correction"),
    )

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="stock_adjustments",)
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPES,)
    quantity = models.DecimalField(max_digits=12, decimal_places=2,)
    reason = models.CharField(max_length=255, blank=True,)
    created_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="stock_adjustments",
    )
    created_at = models.DateTimeField(auto_now_add=True,)    

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            if self.adjustment_type in (
                "OPENING",
                "IN",
            ):
                self.product.current_stock += self.quantity
            elif self.adjustment_type in (
                "OUT",
                "DAMAGE",
            ):
                self.product.current_stock -= self.quantity
            elif self.adjustment_type == "CORRECTION":
                self.product.current_stock = self.quantity
            if self.product.current_stock < 0:
                self.product.current_stock = 0
                
            InventoryTransaction.objects.create(
                product=self.product,
                transaction_type=self.adjustment_type,
                quantity=self.quantity,
                reference=self.reason,
            )

            self.product.save(
                update_fields=("current_stock",),
            )
            
    def __str__(self):
            return f"{self.product.name} - {self.adjustment_type} - {self.quantity}"

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = (
        ("OPENING", "Opening Stock"),
        ("SALE", "Customer Sale"),
        ("STOCK_IN", "Stock In"),
        ("DAMAGE", "Damaged Stock"),
        ("CORRECTION", "Correction"),
    )

    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="inventory_transactions",
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES,)
    quantity = models.DecimalField(max_digits=12, decimal_places=2,)
    reference = models.CharField(max_length=255, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return (
            f"{self.product.name} - "
            f"{self.transaction_type}"
        )