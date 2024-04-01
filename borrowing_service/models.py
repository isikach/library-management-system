from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from book_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ManyToManyField(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    class Meta:
        ordering = ["-expected_return_date",]

    def __str__(self):
        return f"Borrowing #{self.id}"

    def clean(self):
        if self.borrow_date > self.expected_return_date:
            raise ValidationError("expected_return_date must be after borrow_date")
