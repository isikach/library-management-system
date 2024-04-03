import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from book_service.models import Book
from borrowing_service.models import Borrowing
from payment_service.models import Payment


def sample_payment(**params):
    if not (user := params.pop("user", None)):
        user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test12345",
            telegram_id=1,
            is_active=True,
        )

    borrowing = Borrowing.objects.create(
        expected_return_date=datetime.date.today() + datetime.timedelta(days=3),
        book=Book.objects.create(
            title="Test book",
            daily_fee=3.33,
            inventory=1
        ),
        user=user
    )
    defaults = {"borrowing": borrowing}
    defaults.update(params)

    return Payment.objects.create(**defaults)


class PaymentModelTest(TestCase):

    def setUp(self):
        self.payment = sample_payment()

    def test_payment_str(self):
        self.assertEqual(
            str(self.payment),
            f"Payment ID: {self.payment.id} - Status: {self.payment.status}"
        )
