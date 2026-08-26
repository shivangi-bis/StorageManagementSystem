from django.db import models
from products.models import Product


class Inventory(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.product.name
    