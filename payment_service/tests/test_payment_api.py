import datetime
from unittest.mock import patch

import stripe
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from borrowing_service.models import Borrowing
from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer
from payment_service.tests.test_model import sample_payment

PAYMENT_URL = reverse("payment_service:payment-list")
SUCCESS_PAYMENT_URL = reverse("payment_service:payment-success")
CANCEL_PAYMENT_URL = reverse("payment_service:payment-cancel")


def detail_url(payment_id):
    return reverse("payment_service:payment-detail", args=[payment_id])


class UnauthenticatedPaymentApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PAYMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPaymentApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test12345",
            telegram_id=1,
            is_active=True,
        )
        self.borrowing = Borrowing.objects.create(
            expected_return_date=datetime.date.today() + datetime.timedelta(days=5),
            book=Book.objects.create(
                title="Test book",
                daily_fee=5,
                inventory=1
            ),
            user=self.user
        )
        self.payment = sample_payment(user=self.user)

        self.client.force_authenticate(self.user)

    def test_payment_list(self):
        res = self.client.get(PAYMENT_URL)

        payments = Payment.objects.filter(borrowing__user=self.user)
        serializer = PaymentSerializer(payments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_payment_retrieve(self):
        res = self.client.get(detail_url(self.payment.id))

        serializer = PaymentSerializer(self.payment)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_payment_forbidden(self):
        data = {"borrowing": self.borrowing}
        response = self.client.post(PAYMENT_URL, data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch("payment_service.utils.services.PaymentService.set_status_as_paid")
    def test_valid_success_payment(self, mock_set_status_as_paid):
        query_params = {"session_id": "test_session_id"}

        res = self.client.get(SUCCESS_PAYMENT_URL, data=query_params)

        mock_set_status_as_paid.assert_called_once_with("test_session_id")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.user.email, res.data["message"])

    @patch("payment_service.utils.services.PaymentService.set_status_as_paid")
    def test_invalid_success_payment(self, mock_set_status_as_paid):
        mock_set_status_as_paid.side_effect = stripe.error.InvalidRequestError("Invalid request", None)
        query_params = {"session_id": "test_session_id"}

        res = self.client.get(SUCCESS_PAYMENT_URL, data=query_params)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error"], "Invalid request")

    def test_cancel_payment(self):
        res = self.client.get(CANCEL_PAYMENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"info": "You have 24 hours to pay your borrowing"})


class AdminPaymentApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@admin.com",
            password="admin12345",
            telegram_id=1,
        )
        self.borrowing = Borrowing.objects.create(
            expected_return_date=datetime.date.today() + datetime.timedelta(days=5),
            book=Book.objects.create(
                title="Test book",
                daily_fee=5,
                inventory=2
            ),
            user=self.user
        )
        self.payment = sample_payment(user=self.user)

        self.client.force_authenticate(self.user)

    def test_update_payment_not_allowed(self):
        data = {"borrowing": self.borrowing}

        res = self.client.put(detail_url(self.payment.id), data)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_payment_not_allowed(self):
        res = self.client.delete(detail_url(self.payment.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
