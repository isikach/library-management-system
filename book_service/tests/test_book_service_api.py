from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from book_service.serializers import BookSerializer

BOOK_LIST_URL = reverse("books_service:book-list")


def sample_book(**params):
    defaults = {
        "title": "Sample book",
        "author": "Sample author",
        "cover": "Hard",
        "inventory": 2,
        "daily_fee": 2.00,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class UnauthenticatedBookAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_book(self):
        sample_book()
        sample_book()
        response = self.client.get(BOOK_LIST_URL)

        books = Book.objects.all().order_by("id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        payload = {
            "title": "Sample book1",
            "author": "Sample author1",
            "cover": "Hard",
            "inventory": 2,
            "daily_fee": 2.00,
        }
        response = self.client.post(BOOK_LIST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin.user@mail.com",
            password="1qazcde3",
            first_name="Bob",
            last_name="Smith",
        )
        self.client.force_authenticate(self.user)

    def test_list_book(self):
        sample_book()
        sample_book()
        response = self.client.get(BOOK_LIST_URL)

        books = Book.objects.all().order_by("id")
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        payload = {
            "title": "Sample book1",
            "author": "Sample author1",
            "cover": "Hard",
            "inventory": 2,
            "daily_fee": 2.00,
        }
        response = self.client.post(BOOK_LIST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserBookAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin.user@mail.com",
            password="1qazcde3",
            first_name="Bob",
            last_name="Smith",
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "Sample book1",
            "author": "Sample author1",
            "cover": "Hard",
            "inventory": 2,
            "daily_fee": 2.00,
        }
        response = self.client.post(BOOK_LIST_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
