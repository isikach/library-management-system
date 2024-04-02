import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from book_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True,)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True,)
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name="borrowings",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="borrowings",
    )

    class Meta:
        ordering = ["-expected_return_date",]

    def __str__(self):
        return f"Borrowing #{self.id}"

    @staticmethod
    def get_next_return_date(book_id: int) -> datetime.date|None:
        current_date = datetime.date.today()

        next_borrowing = Borrowing.objects.filter(
            book_id=book_id,
            expected_return_date__gt=current_date,
        ).order_by("-expected_return_date").first()

        return next_borrowing.expected_return_date

    @staticmethod
    def validate_book_inventory(inventory: int, book_title: str, book_id: int):
        if inventory == 0:
            next_return_date = Borrowing.get_next_return_date(book_id)
            raise ValidationError(
                f"All '{book_title}' books are currently borrowed"
                f" Come back on {next_return_date}"
            )

    def clean(self):
        if self.borrow_date > self.expected_return_date:
            raise ValidationError("expected_return_date must be after borrow_date")

        Borrowing.validate_book_inventory(self.book.inventory, self.book.title, self.book.id)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )
