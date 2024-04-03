import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer
)
from borrowing_service.tests.test_model import sample_borrowing

BORROWING_URL = reverse("borrowing_service:borrowing-list")


class UnauthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_borrowing_for_users_borrowings_only(self):
        sample_borrowing(user=self.user),
        sample_borrowing(
            user=get_user_model().objects.create_user(
                email="test1@test.com",
                password="test12345"
            )
        )

        res = self.client.get(BORROWING_URL)
        borrowings = Borrowing.objects.all()

        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data, serializer.data)

    def test_borrowing_creation(self):
        book = Book.objects.create(
            title="test",
            author="test",
            cover="soft",
            inventory=1,
            daily_fee=2,
        )

        data1 = {
            "expected_return_date": datetime.date.fromisoformat("2024-04-04"),
            "book": book.id
        }
        data2 = {
            "expected_return_date": datetime.date.fromisoformat("2024-04-05"),
            "book": book.id
        }
        data3 = {
            "expected_return_date": datetime.date.fromisoformat("2024-04-01")
        }

        res1 = self.client.post(BORROWING_URL, data1, format="json")
        res2 = self.client.post(BORROWING_URL, data2, format="json")
        res3 = self.client.post(BORROWING_URL, data3, format="json")

        self.assertEqual(res1.status_code, status.HTTP_302_FOUND)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_borrowing(self):
        borrowing = sample_borrowing(user=self.user)

        res = self.client.get(
            reverse(
                "borrowing_service:borrowing-detail",
                args=[borrowing.id]
            )
        )

        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_is_active_filtering(self):
        borrowing1 = sample_borrowing(user=self.user)
        borrowing2 = sample_borrowing(
            user=self.user,
            actual_return_date=datetime.date.today()
        )

        res = self.client.get(BORROWING_URL, {"is_active": "true"})

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_return_borrowing_that_is_already_returned(self):
        borrowing = sample_borrowing(
            user=self.user,
            actual_return_date=datetime.date.today()
        )

        res = self.client.post(reverse("borrowing_service:borrowing-return-borrowing", args=[borrowing.id]))

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_borrowing_is_success(self):
        borrowing = sample_borrowing(user=self.user)
        borrowing.expected_return_date = datetime.date.fromisoformat("2024-04-06")
        inventory = borrowing.book.inventory

        self.client.post(reverse("borrowing_service:borrowing-return-borrowing", args=[borrowing.id]))

        borrowing.refresh_from_db()
        self.assertEqual(borrowing.actual_return_date, datetime.date.today())

        borrowing.book.refresh_from_db()
        self.assertEqual(borrowing.book.inventory, inventory + 1)

    def test_return_overdue_borrowing(self):
        borrowing = sample_borrowing(user=self.user)
        borrowing.borrow_date = datetime.date.fromisoformat("2024-03-29")
        borrowing.expected_return_date = datetime.date.fromisoformat("2024-04-01")

        res = self.client.post(reverse("borrowing_service:borrowing-return-borrowing", args=[borrowing.id]))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        borrowing.refresh_from_db()
        self.assertEqual(borrowing.actual_return_date, datetime.date.today())


class AdminBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test12345",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_user_id_filtering(self):
        user1 = get_user_model().objects.create_user(
            email="test1@test.com",
            password="test12345"
        )
        user2 = get_user_model().objects.create_user(
            email="test2@test.com",
            password="test12345"
        )
        borrowing1 = sample_borrowing(user=user1)
        borrowing2 = sample_borrowing(user=user2)

        res = self.client.get(BORROWING_URL, {"user_id": user1.id})

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
