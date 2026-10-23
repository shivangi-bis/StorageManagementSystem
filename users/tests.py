
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


class UserPermissionTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="testadmin",
            password="TestPass123!",
            role="admin",
        )

        self.staff = User.objects.create_user(
            username="teststaff",
            password="TestPass123!",
            role="staff",
        )

        self.user_list_url = reverse("user-list")
        self.staff_detail_url = reverse(
            "user-detail",
            kwargs={"pk": self.staff.pk},
        )

    def test_staff_cannot_view_all_users(self):
        self.client.force_authenticate(user=self.staff)

        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_cannot_create_users(self):
        self.client.force_authenticate(user=self.staff)

        response = self.client.post(
            self.user_list_url,
            {
                "username": "newstaff",
                "email": "newstaff@example.com",
                "password": "TestPass123!",
                "role": "staff",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_view_own_details(self):
        self.client.force_authenticate(user=self.staff)

        response = self.client.get(self.staff_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_cannot_delete_users(self):
        self.client.force_authenticate(user=self.staff)

        response = self.client.delete(self.staff_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
