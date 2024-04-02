from django.test import TestCase

from book_service.models import Book


class BookModelTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="At the Mountains of Madness",
            author="Howard Phillips Lovecraft",
            cover="Hard",
            inventory=6,
            daily_fee=6.00,
        )

    def test_user_str(self):
        self.assertEqual(
            str(self.book),
            f"{self.book.title}"
        )

    def test_book_fields_quantity(self):
        expected_fields = [
            "id", "title", "author", "cover", "inventory", "daily_fee"
        ]
        model_fields = [
            field.name
            for field in Book._meta.fields
        ]

        for field in expected_fields:
            self.assertIn(field, model_fields)
