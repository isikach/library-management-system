from celery import shared_task
from notification_service.telegram_bot import BookBorrowingBot

bot = BookBorrowingBot()


@shared_task
def send_test_message():
    bot.send_test_message()
