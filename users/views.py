
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .permissions import Isadmin
from .models import User
from .serializers import UserSerializer


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only admins can view all users.
        if not Isadmin().has_permission(request, self):
            return Response(
                {"detail": "Only Admin can view all users."},
                status=status.HTTP_403_FORBIDDEN
            )

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not Isadmin().has_permission(request, self):
            return Response(
                {"detail": "Only Admin can create users."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_authorized_user(self, request, pk):
        # Admin can access any user; staff can access only themselves.
        if request.user.role == "admin":
            return get_object_or_404(User, pk=pk)

        return get_object_or_404(User, pk=pk, id=request.user.id)

    def get(self, request, pk):
        user = self.get_authorized_user(request, pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        if not Isadmin().has_permission(request, self):
            return Response(
                {"detail": "Only Admin can update users."},
                status=status.HTTP_403_FORBIDDEN
            )

        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        if not Isadmin().has_permission(request, self):
            return Response(
                {"detail": "Only Admin can update users."},
                status=status.HTTP_403_FORBIDDEN
            )

        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        if not Isadmin().has_permission(request, self):
            return Response(
                {"detail": "Only Admin can delete users."},
                status=status.HTTP_403_FORBIDDEN
            )

        user = get_object_or_404(User, pk=pk)
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
