import unittest
from unittest.mock import MagicMock
from telegram_bot import BookBorrowingBot


class TestBookBorrowingBot(unittest.TestCase):
    def setUp(self) -> None:
        self.bot = BookBorrowingBot()

    def test_send_welcome(self) -> None:
        message = MagicMock()
        message.text = "start"
        message.chat.id = 123

        self.bot.send_welcome(message)
        self.bot.bot.reply_to.assert_called_once_with(
            message,
            "Hi! I can help you to manage your book borrowing. First write your e-mail"
        )

    def test_get_user_chat_id_existing_user(self) -> None:
        message = MagicMock()
        message.text = "user@example.com"
        message.chat.id = 123

        user = MagicMock()
        user.telegram_id = 123
        user.is_active = False

        get_user_model = MagicMock(return_value=MagicMock())
        get_user_model().objects.get.return_value = user
        self.bot.get_user_model = get_user_model

        self.bot.bot.send_message = MagicMock()

        self.bot.get_user_chat_id(message)
        self.assertTrue(user.is_active)
        self.assertTrue(user.save.called)
        self.bot.bot.send_message.assert_called_once_with(
            123,
            "Now you can get info from our service"
        )

    def test_get_user_chat_id_nonexistent_user(self) -> None:
        message = MagicMock()
        message.text = "invalid@example.com"
        message.chat.id = 123
        get_user_model = MagicMock(return_value=MagicMock())
        get_user_model().objects.get.side_effect = get_user_model().DoesNotExist

        self.bot.get_user_model = get_user_model

        self.bot.bot.send_message = MagicMock()

        self.bot.get_user_chat_id(message)
        self.bot.bot.send_message.assert_called_once_with(
            123,
            "Please enter a valid e-mail")
