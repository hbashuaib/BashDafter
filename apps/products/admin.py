from django.contrib import admin

from .models import (
    Category,
    Product,
    Unit,
)

admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Product)