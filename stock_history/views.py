from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import StockMovement
from .serializers import StockMovementSerializer


class StockMoveListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        movements = StockMovement.objects.all().order_by(
            "-created_at"
        )

        serializer = StockMovementSerializer(
            movements,
            many=True
        )

        return Response(serializer.data)
    