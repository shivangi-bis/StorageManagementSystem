from django.db import models

from products.models import Product

class StockMovement(models.Model):

    MOVEMENT_TYPES = (
        ('IN', 'Stock In'),
        ('OUT','Stock Out'),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )

    quantity = models.PositiveIntegerField()

    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_TYPES
    )

    reason = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.product.name}-"
            f"{self.movement_type}-"
            f"{self.quantity}"
        )