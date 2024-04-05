from celery import shared_task
from notification_service.telegram_bot import BookBorrowingBot
from notification_service.users_with_overdue import notification_about_overdue

bot = BookBorrowingBot()


@shared_task
def send_test_message():
    bot.send_test_message()
    notification_about_overdue()
