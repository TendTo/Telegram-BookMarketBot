# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods,redefined-outer-name,redefined-builtin
"""Tests for the bot commands"""
from datetime import datetime
import pytest
from pytest_mock import MockerFixture
import bs4
from telegram import Update, User, Message, Chat, Bot
from telegram.ext import CallbackContext, Updater
from module.sell import sell, SELL_USAGE, ISBN_ERROR, USERNAME_ERROR, SEARCHING_ISBN
from module.shared import BOOK_NOT_AVAILABLE, ON_SALE_CONFIRM
from module.start import start, START_MESSAGE
from module.help import help, HELP_MESSAGE
from tests.constants import (
    DEFAULT_MESSAGE_REPLY_KWARGS,
    ISBN_10,
    ISBN_13,
    INTEGER_PRICE,
    COMMA_PRICE,
    DOT_PRICE,
)


class FixtureRequest:
    """Fixture request class used for type hinting"""

    param: str


@pytest.fixture(scope="function", params=["username"])
def mocked_bot(request: FixtureRequest, mocker: MockerFixture) -> Bot:
    """Creates a mocked Bot instance
    By default, if the :meth:`get_chat` method is called, it will return a
    dictionary with the key `username` set to `username`.
    To change this behavior, use the following decorator on top of the test method:
    ```python
    @pytest.mark.parametrize("mocked_bot", ["new username"], indirect=True)
    def test_method(self, update: Update, context: CallbackContext):
        ... # test code
    ```
    """
    bot = mocker.Mock(return_value=None)
    mocker.patch.object(bot, "get_chat", side_effect=lambda _: {"username": request.param})
    return bot


@pytest.fixture(scope="function")
def context(mocked_bot: Bot) -> CallbackContext:
    """Creates a Telegram CallbackContext.
    The bot is mocked, meaning every method used will not produce any effect.
    This also allows to check how many time a method has been called and with what args"""
    updater = Updater(token="1234567890:abcdefghijklmnopqrstuvwxyz123456789")
    dispatcher = updater.dispatcher
    dispatcher.bot = mocked_bot
    return CallbackContext(dispatcher)


@pytest.fixture(scope="function", params=[Chat.GROUP])
def update(request: FixtureRequest, mocked_bot: Bot) -> Update:
    """Creates a Telegram Update object, caused by a message being sent.
    By default, the message is treated as being sent in a group chat.
    To change this behavior, use the following decorator on top of the test method:
    ```python
    @pytest.mark.parametrize("update", [Chat.PRIVATE, Chat.CHANNEL], indirect=True)
    def test_method(self, update: Update, context: CallbackContext):
        ... # test code
    ```
    """
    chat = Chat(id=0, type=request.param)
    user = User(id=0, first_name="user", is_bot=False, username="user")
    message = Message(message_id=0, from_user=user, chat=chat, date=datetime.now())
    message.bot = mocked_bot
    return Update(update_id=0, message=message)


class TestCommands:
    class TestBaseCommands:
        def test_start_cmd(self, update: Update, context: CallbackContext):
            start(update, context)
            context.bot.send_message.assert_called_once_with(
                **DEFAULT_MESSAGE_REPLY_KWARGS,
                chat_id=update.message.chat_id,
                text=START_MESSAGE,
            )

        def test_help_cmd(self, update: Update, context: CallbackContext):
            help(update, context)
            context.bot.send_message.assert_called_once_with(
                **DEFAULT_MESSAGE_REPLY_KWARGS,
                chat_id=update.message.chat_id,
                text=HELP_MESSAGE,
            )

    class TestSellCommand:
        def mock_sell_functions(
            self, mocker: MockerFixture, find_return: tuple = (), book_return: tuple = ()
        ):
            soup = mocker.Mock(spec=bs4.BeautifulSoup)
            soup.find.return_value = mocker.Mock(text="title/author")
            mocker.patch("module.sell.find", return_value=[find_return] if find_return else [])
            mocker.patch("module.sell.add_item")
            mocker.patch("module.sell.add_book")
            mocker.patch(
                "module.sell.book_in_unict", return_value=book_return if book_return else []
            )
            mocker.patch("module.sell.get_book_info", side_effect=lambda *args: args)
            mocker.patch("module.sell._get_isbn_from_website", side_effect=lambda *args: args)

        def test_sell_cmd_usage(self, update: Update, context: CallbackContext):
            update.message.text = "/vendi"
            sell(update, context)
            context.bot.send_message.assert_called_once_with(update.message.chat_id, SELL_USAGE)

        @pytest.mark.parametrize("isbn", [ISBN_10, ISBN_13])
        @pytest.mark.parametrize("price", [INTEGER_PRICE, DOT_PRICE, COMMA_PRICE])
        @pytest.mark.parametrize("mocked_bot", [None], indirect=True)
        def test_sell_cmd_no_username(
            self, update: Update, context: CallbackContext, isbn: str, price: str
        ):
            update.message.text = f"/vendi {isbn} {price}"
            sell(update, context)
            context.bot.send_message.assert_called_once_with(update.message.chat_id, USERNAME_ERROR)

        def test_sell_cmd_invalid_ISBN(self, update: Update, context: CallbackContext):
            update.message.text = "/vendi 1"
            sell(update, context)
            context.bot.send_message.assert_called_once_with(update.message.chat_id, ISBN_ERROR)

        @pytest.mark.parametrize("isbn", [ISBN_10, ISBN_13])
        @pytest.mark.parametrize("price", [INTEGER_PRICE, DOT_PRICE, COMMA_PRICE])
        def test_sell_cmd_find_in_local_db(
            self,
            mocker: MockerFixture,
            update: Update,
            context: CallbackContext,
            isbn: str,
            price: str,
        ):
            find_return = (isbn, "title", "author")
            self.mock_sell_functions(mocker, find_return=find_return)
            update.message.text = f"/vendi {isbn} {price}"
            sell(update, context)

            calls = (
                mocker.call(update.message.chat_id, SEARCHING_ISBN),
                mocker.call(update.message.chat_id, find_return),
                mocker.call(update.message.chat_id, ON_SALE_CONFIRM),
            )
            context.bot.send_message.assert_has_calls(calls)

        @pytest.mark.parametrize("isbn", [ISBN_10, ISBN_13])
        @pytest.mark.parametrize("price", [INTEGER_PRICE, DOT_PRICE, COMMA_PRICE])
        def test_sell_cmd_book_in_unict_not_found(
            self,
            mocker: MockerFixture,
            update: Update,
            context: CallbackContext,
            isbn: str,
            price: str,
        ):
            self.mock_sell_functions(mocker, book_return=(False, None))
            update.message.text = f"/vendi {isbn} {price}"
            sell(update, context)

            calls = (
                mocker.call(update.message.chat_id, SEARCHING_ISBN),
                mocker.call(update.message.chat_id, BOOK_NOT_AVAILABLE),
            )
            context.bot.send_message.assert_has_calls(calls)

        @pytest.mark.parametrize("isbn", [ISBN_10, ISBN_13])
        @pytest.mark.parametrize("price", [INTEGER_PRICE, DOT_PRICE, COMMA_PRICE])
        def test_sell_cmd_book_in_unict_found(
            self,
            mocker: MockerFixture,
            update: Update,
            context: CallbackContext,
            isbn: str,
            price: str,
        ):
            find_return = (isbn, "title", "author")
            self.mock_sell_functions(mocker, find_return=find_return, book_return=(True, "soup"))
            update.message.text = f"/vendi {isbn} {price}"
            sell(update, context)

            calls = (
                mocker.call(update.message.chat_id, SEARCHING_ISBN),
                mocker.call(update.message.chat_id, find_return),
                mocker.call(update.message.chat_id, ON_SALE_CONFIRM),
            )
            context.bot.send_message.assert_has_calls(calls)
