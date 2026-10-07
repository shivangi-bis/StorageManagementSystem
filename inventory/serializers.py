from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.ModelSerializer):

    low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            'id',
            'product',
            'quantity',
            'updated_at',
            'low_stock',
        ]

    def get_low_stock(self, obj):
        return obj.quantity <= 5