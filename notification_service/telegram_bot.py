import os

import telebot
import django
from django.contrib.auth import get_user_model


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_management_system.settings")
django.setup()


class BookBorrowingBot:
    API_TOKEN = os.environ.get("API_TOKEN")

    def __init__(self) -> None:
        self.bot = telebot.TeleBot(self.API_TOKEN)
        self.bot.message_handler(commands=["start"])(self.send_welcome)
        self.bot.message_handler(content_types=["text"])(self.get_user_chat_id)

    def send_welcome(self, message: telebot.types.Message) -> None:
        self.bot.reply_to(message, "Hi! I can help you to manage your book borrowing. "
                                   "First write your e-mail")

    def get_user_chat_id(self, message: telebot.types.Message) -> None:
        email = message.text
        chat_id = message.chat.id

        try:
            user = get_user_model().objects.get(email=email)
            user.telegram_id = chat_id
            user.is_active = True
            user.save()
            self.bot.send_message(chat_id, "Now you can get info from our service")
        except get_user_model().DoesNotExist:
            self.bot.send_message(chat_id, "Please enter a valid e-mail")

    def create_borrowing_notification(
            self,
            title: str,
            user: get_user_model()
    ) -> None:
        chat_id = user.telegram_id
        self.bot.send_message(
            chat_id,
            f"Book {title} borrows successfully!"
        )

    def success_payment_notification(
            self,
            user: get_user_model()
    ) -> None:
        chat_id = user.telegram_id
        self.bot.send_message(
            chat_id,
            "Your payment approved successfully!"
        )

    def start_polling(self) -> None:
        self.bot.polling()


if __name__ == "__main__":
    bot = BookBorrowingBot()
    bot.start_polling()
