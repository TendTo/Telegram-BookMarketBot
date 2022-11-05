from telegram.utils.helpers import DEFAULT_NONE


DEFAULT_MESSAGE_REPLY_KWARGS = {
    "parse_mode": DEFAULT_NONE,
    "disable_web_page_preview": DEFAULT_NONE,
    "disable_notification": DEFAULT_NONE,
    "reply_to_message_id": None,
    "reply_markup": None,
    "timeout": DEFAULT_NONE,
    "api_kwargs": None,
    "allow_sending_without_reply": DEFAULT_NONE,
    "entities": None,
}

SELECT_QUERY = "SELECT * FROM Books WHERE ISBN=?"
INSERT_QUERY = "INSERT INTO Books(ISBN, Title, Authors) VALUES(?,?,?)"
DELETE_QUERY = "DELETE FROM Market WHERE rowid=?"
ISBN_13 = "9783161482946"
ISBN_10 = "3161482948"

INTEGER_PRICE = "15"
DOT_PRICE = "15.50"
COMMA_PRICE = "15,50"
