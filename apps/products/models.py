from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True,)
    description = models.TextField(blank=True,)
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True,)
    description = models.TextField(blank=True,)
    created_at = models.DateTimeField(auto_now_add=True, )

    def __str__(self):
        return self.name


class Product(models.Model):
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, related_name='products',)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True,)
    name = models.CharField(max_length=255,)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True,)
    description = models.TextField(blank=True,)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    minimum_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    current_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0,)
    has_expiry = models.BooleanField(default=False,)
    expiry_date = models.DateField(blank=True, null=True,)
    is_active = models.BooleanField(default=True,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    
    @property
    def is_low_stock(self):
        return (
            self.current_stock
            <= self.minimum_stock
        )

    def __str__(self):
        return self.name