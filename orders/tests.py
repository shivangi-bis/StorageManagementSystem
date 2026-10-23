
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from products.models import Product
from inventory.models import Inventory
from orders.models import Order
from stock_history.models import StockMovement


class OrderStockTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="order_test_user",
            password="TestPass123!",
            role="staff",
        )
        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(
            name="Test Laptop",
            description="Laptop for testing",
            price="50000.00",
            category="Electronics",
        )

        self.inventory = Inventory.objects.create(
            product=self.product,
            quantity=10,
        )

        self.order_url = reverse("order-list")

    def test_creating_order_reduces_stock(self):
        response = self.client.post(
            self.order_url,
            {
                "product": self.product.pk,
                "quantity": 3,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 7)

        self.assertTrue(
            Order.objects.filter(
                product=self.product,
                quantity=3,
                user=self.user,
            ).exists()
        )

        self.assertTrue(
            StockMovement.objects.filter(
                product=self.product,
                quantity=3,
                movement_type="OUT",
                reason="Order created",
            ).exists()
        )

    def test_insufficient_stock_rejects_order(self):
        response = self.client.post(
            self.order_url,
            {
                "product": self.product.pk,
                "quantity": 11,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 10)
        self.assertEqual(Order.objects.count(), 0)

    def test_deleting_order_restores_stock(self):
        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=4,
        )

        self.inventory.quantity = 6
        self.inventory.save()

        delete_url = reverse(
            "order-detail",
            kwargs={"pk": order.pk},
        )

        response = self.client.delete(delete_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 10)
        self.assertFalse(
            Order.objects.filter(pk=order.pk).exists()
        )

        self.assertTrue(
            StockMovement.objects.filter(
                product=self.product,
                quantity=4,
                movement_type="IN",
                reason="Order deleted",
            ).exists()
        )
