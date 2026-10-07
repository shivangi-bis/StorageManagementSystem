from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer
from inventory.models import Inventory
from stock_history.models import StockMovement


class OrderListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = Order.objects.all()

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = OrderSerializer(
            data=request.data
        )

        if serializer.is_valid():

            product = serializer.validated_data["product"]

            order_quantity = serializer.validated_data[
                "quantity"
            ]

            inventory = get_object_or_404(
                Inventory,
                product=product
            )

            if inventory.quantity < order_quantity:

                return Response(
                    {"detail": "Insufficient stock."},
                    status=400
                )

            with transaction.atomic():

                order = serializer.save(
                    user=request.user
                )

                inventory.quantity -= order_quantity
                inventory.save()

                StockMovement.objects.create(
                    product=product,
                    quantity=order_quantity,
                    movement_type="OUT",
                    reason="Order created"
                )

            return Response(
                OrderSerializer(order).data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


class OrderDetailView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request, pk):

        order = get_object_or_404(
            Order,
            id=pk
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data)


    def put(self, request, pk):

        order = get_object_or_404(
            Order,
            id=pk
        )

        old_quantity = order.quantity

        serializer = OrderSerializer(
            order,
            data=request.data
        )

        if serializer.is_valid():

            new_quantity = serializer.validated_data[
                "quantity"
            ]

            difference = (
                new_quantity - old_quantity
            )

            inventory = get_object_or_404(
                Inventory,
                product=order.product
            )

            if difference > 0:

                if inventory.quantity < difference:

                    return Response(
                        {
                            "detail":
                            "Insufficient stock."
                        },
                        status=400
                    )

            with transaction.atomic():

                serializer.save()

                inventory.quantity -= difference
                inventory.save()

                if difference > 0:

                    StockMovement.objects.create(
                        product=order.product,
                        quantity=difference,
                        movement_type="OUT",
                        reason="Order quantity increased"
                    )

                elif difference < 0:

                    StockMovement.objects.create(
                        product=order.product,
                        quantity=abs(difference),
                        movement_type="IN",
                        reason="Order quantity reduced"
                    )

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )


    def patch(self, request, pk):

        order = get_object_or_404(
            Order,
            id=pk
        )

        old_quantity = order.quantity

        serializer = OrderSerializer(
            order,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            new_quantity = (
                serializer.validated_data.get(
                    "quantity",
                    old_quantity
                )
            )

            difference = (
                new_quantity - old_quantity
            )

            inventory = get_object_or_404(
                Inventory,
                product=order.product
            )

            if difference > 0:

                if inventory.quantity < difference:

                    return Response(
                        {
                            "detail":
                            "Insufficient stock."
                        },
                        status=400
                    )

            with transaction.atomic():

                serializer.save()

                inventory.quantity -= difference
                inventory.save()

                if difference > 0:

                    StockMovement.objects.create(
                        product=order.product,
                        quantity=difference,
                        movement_type="OUT",
                        reason="Order quantity increased"
                    )

                elif difference < 0:

                    StockMovement.objects.create(
                        product=order.product,
                        quantity=abs(difference),
                        movement_type="IN",
                        reason="Order quantity reduced"
                    )

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )


    def delete(self, request, pk):

        order = get_object_or_404(
            Order,
            id=pk
        )

        inventory = get_object_or_404(
            Inventory,
            product=order.product
        )

        with transaction.atomic():

            inventory.quantity += order.quantity
            inventory.save()

            StockMovement.objects.create(
                product=order.product,
                quantity=order.quantity,
                movement_type="IN",
                reason="Order deleted"
            )

            order.delete()

        return Response(
            {
                "detail":
                "Order deleted successfully."
            },
            status=204
        )