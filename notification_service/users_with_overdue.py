from typing import List

from django.contrib.auth import get_user_model
from django.utils import timezone

from notification_service.telegram_bot import BookBorrowingBot
from user.models import User
from borrowing_service.models import Borrowing


def get_overdue_users() -> List[User]:
    today = timezone.now().date()
    overdue_borrowers = Borrowing.objects.filter(
        actual_return_date__isnull=True,
        expected_return_date__lt=today
    )
    overdue_users = overdue_borrowers.values_list("user", flat=True).distinct()
    users_with_overdue_borrowings = get_user_model().objects.filter(id__in=overdue_users)

    return users_with_overdue_borrowings


def get_overdue_books_for_user(user_id: int) -> str:
    today = timezone.now().date()
    overdue_borrowings = Borrowing.objects.filter(
        user_id=user_id,
        actual_return_date__isnull=True,
        expected_return_date__lt=today
    )
    overdue_books_titles = [borrowing.book.title for borrowing in overdue_borrowings]
    return "\n".join(overdue_books_titles)


def notification_about_overdue() -> None:
    overdue_users = get_overdue_users()
    for user in overdue_users:
        books = get_overdue_books_for_user(user.id)
        BookBorrowingBot().overdue_borrowing_notification(
            user=user, books=books)
