from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import Isadmin

from .models import User
from .serializers import UserSerializer

class UserListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):

        if not Isadmin().has_permission(request, self):
            return Response(
                {"detail": "Only Admin can create users."},
                status=403
            )
        
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

class UserDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = User.objects.get(id=pk)

        serializer = UserSerializer(
            user,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
 
    def patch(self, request, pk):
        user = User.objects.get(id=pk)

        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        user.delete()

        return Response(
            {"detail": "User deleted successfully."},
            status=204
        )