from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Inventory
from .serializers import InventorySerializer
from stock_history.models import StockMovement


class InventoryListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        inventory = Inventory.objects.all()

        serializer = InventorySerializer(
            inventory,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = InventorySerializer(
            data=request.data
        )

        if serializer.is_valid():

            inventory = serializer.save()

            StockMovement.objects.create(
                product=inventory.product,
                quantity=inventory.quantity,
                movement_type="IN",
                reason="Initial stock added"
            )

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


class InventoryDetailView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request, pk):

        inventory = Inventory.objects.get(id=pk)

        serializer = InventorySerializer(
            inventory
        )

        return Response(serializer.data)


    def put(self, request, pk):

        inventory = Inventory.objects.get(id=pk)

        old_quantity = inventory.quantity

        serializer = InventorySerializer(
            inventory,
            data=request.data
        )

        if serializer.is_valid():

            updated_inventory = serializer.save()

            quantity_difference = (
                updated_inventory.quantity
                - old_quantity
            )

            if quantity_difference > 0:

                StockMovement.objects.create(
                    product=updated_inventory.product,
                    quantity=quantity_difference,
                    movement_type="IN",
                    reason="Inventory updated"
                )

            elif quantity_difference < 0:

                StockMovement.objects.create(
                    product=updated_inventory.product,
                    quantity=abs(
                        quantity_difference
                    ),
                    movement_type="OUT",
                    reason="Inventory reduced"
                )

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )


    def patch(self, request, pk):

        inventory = Inventory.objects.get(id=pk)

        old_quantity = inventory.quantity

        serializer = InventorySerializer(
            inventory,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_inventory = serializer.save()

            quantity_difference = (
                updated_inventory.quantity
                - old_quantity
            )

            if quantity_difference > 0:

                StockMovement.objects.create(
                    product=updated_inventory.product,
                    quantity=quantity_difference,
                    movement_type="IN",
                    reason="Inventory updated"
                )

            elif quantity_difference < 0:

                StockMovement.objects.create(
                    product=updated_inventory.product,
                    quantity=abs(
                        quantity_difference
                    ),
                    movement_type="OUT",
                    reason="Inventory reduced"
                )

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )


    def delete(self, request, pk):

        inventory = Inventory.objects.get(id=pk)

        inventory.delete()

        return Response(
            status=204
        )