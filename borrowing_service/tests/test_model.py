import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from book_service.models import Book
from borrowing_service.models import Borrowing


def sample_borrowing(**params):
    defaults = {
        "borrow_date": datetime.date.today(),
        "expected_return_date": datetime.date.today(),
        "book": Book.objects.create(
            title="test",
            author="test",
            cover="soft",
            inventory=1,
            daily_fee=2,
        ),
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.borrowing = sample_borrowing(
            user=get_user_model().objects.create_user(
                email="test@test.com",
                password="test12345"
            )
        )

    def test_str_method(self):
        self.assertEqual(str(self.borrowing), f"Borrowing #{self.borrowing.id}")

    def test_clean_method(self):
        with self.assertRaises(ValidationError):
            sample_borrowing(
                expected_return_date=datetime.date.fromisoformat("2024-04-01"),
                user=get_user_model().objects.create_user(
                    email="test1@test.com",
                    password="test12345"
                )
            )
