# pylint: disable=missing-class-docstring,missing-function-docstring,too-few-public-methods,redefined-outer-name,redefined-builtin,unused-argument
"""Tests for the db interactions"""
from sqlite3 import Connection, Cursor, DatabaseError
import pytest
from pytest_mock import MockerFixture
from telegram.ext import CallbackContext, Updater
from module.add_item import add_item
from module.find import find, app_find, BOOKS
from module.add_book import add_book
from module.create_connection import (
    connect_and_execute,
    DB_ERROR,
    DELETE,
    INSERT,
    SELECT,
)
from tests.constants import (
    ISBN_10,
    ISBN_13,
    SELECT_QUERY,
    INSERT_QUERY,
    DELETE_QUERY,
)


@pytest.fixture(scope="function")
def conn(mocker: MockerFixture) -> Connection:
    """Mocks the sqlite3.connect method and returns a mocked connection"""
    conn = mocker.MagicMock(spec=Connection)
    conn.__enter__.return_value = conn
    cur = mocker.MagicMock(spec=Cursor)
    mocker.patch("sqlite3.connect", return_value=conn)
    mocker.patch.object(conn, "cursor", return_value=cur)
    return conn


@pytest.fixture(scope="function")
def ctx(mocker: MockerFixture) -> CallbackContext:
    """Creates a Telegram CallbackContext.
    The bot is mocked, meaning every method used will not produce any effect.
    This also allows to check how many time a method has been called and with what args"""
    updater = Updater(token="1234567890:abcdefghijklmnopqrstuvwxyz123456789")
    dispatcher = updater.dispatcher
    dispatcher.bot = mocker.Mock(return_value=None)
    return CallbackContext(dispatcher)


class TestDB:
    class TestCreateConnection:
        def test_create_connection_error(self, conn: Connection, ctx: CallbackContext):
            conn.cursor.side_effect = DatabaseError()
            connect_and_execute(ctx, 0, SELECT_QUERY, ("1234567890",), SELECT)
            ctx.bot.send_message.assert_called_once_with(0, DB_ERROR)

        def test_create_connection_insert(self, conn: Connection, ctx: CallbackContext):
            args = ("1234567890", "Title", "Author")
            connect_and_execute(ctx, 0, INSERT_QUERY, args, INSERT)
            conn.cursor().execute.assert_called_once_with(INSERT_QUERY, args)
            conn.commit.assert_called_once()

        def test_create_connection_delete(self, conn: Connection, ctx: CallbackContext):
            args = ("1234567890",)
            connect_and_execute(ctx, 0, DELETE_QUERY, args, DELETE)
            conn.cursor().execute.assert_called_once_with(DELETE_QUERY, args)
            conn.commit.assert_called_once()

        def test_create_connection_select(self, conn: Connection, ctx: CallbackContext):
            args = ("1234567890",)
            connect_and_execute(ctx, 0, SELECT_QUERY, args, "select")
            conn.cursor().execute.assert_called_once_with(SELECT_QUERY, args)
            conn.cursor().fetchall.assert_called_once()

    class TestSelect:
        @pytest.mark.parametrize("isbn", [ISBN_10, ISBN_13])
        def test_find_mode_book(self, conn: Connection, ctx: CallbackContext, isbn: str):
            find(ctx, 0, isbn, BOOKS)

            query = "SELECT * FROM Books WHERE ISBN=?"
            conn.cursor().execute.assert_called_once_with(query, (isbn,))

        def test_find_mode_market(self, conn: Connection, ctx: CallbackContext):
            find(ctx, 0, "title", "Market")

            query = (
                "SELECT rowid, * FROM Market WHERE Title LIKE ? OR ISBN Like ? OR Authors LIKE ?"
            )
            conn.cursor().execute.assert_called_once_with(query, ("%title%", "%title%", "%title%"))

        @pytest.mark.parametrize("isbn", [ISBN_10, ISBN_13])
        def test_app_find_mode_book(self, conn: Connection, isbn: str):
            app_find(isbn, conn, BOOKS)

            query = "SELECT * FROM Books WHERE ISBN=?"
            conn.cursor().execute.assert_called_once_with(query, (isbn,))

        def test_app_find_mode_market(self, conn: Connection):
            app_find("title", conn, "Market")

            query = (
                "SELECT rowid, * FROM Market WHERE Title LIKE ? OR ISBN Like ? OR Authors LIKE ?"
            )
            conn.cursor().execute.assert_called_once_with(query, ("%title%", "%title%", "%title%"))

    @pytest.mark.parametrize("isbn", [ISBN_10, ISBN_13])
    class TestInsert:
        def test_add_book(self, conn: Connection, ctx: CallbackContext, isbn: str):
            add_book(ctx, 0, isbn, "title", "author")

            query = "INSERT INTO Books(ISBN, Title, Authors) VALUES(?,?,?)"
            conn.cursor().execute.assert_called_once_with(query, (isbn, "title", "author"))

        def test_add_item(self, conn: Connection, ctx: CallbackContext, isbn: str):
            add_item(ctx, 0, isbn, "title", "author", "username", "price")

            query = "INSERT INTO Market(ISBN, Title, Authors, Seller, Price) VALUES(?,?,?,?,?)"
            conn.cursor().execute.assert_called_once_with(
                query, (isbn, "title", "author", "username", "price")
            )
