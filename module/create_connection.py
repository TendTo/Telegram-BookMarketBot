import sqlite3
from module.shared import DB_PATH, DB_ERROR, INSERT, DELETE, SELECT
from telegram.ext import CallbackContext
from typing import Literal, Optional, Union

def create_connection(db_file: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(str(e))
    return conn

def connect_and_execute(
    context: CallbackContext,
    chat_id: int,
    query: str,
    params: tuple,
    operation: Literal["insert", "delete", "select"],
) -> Optional[Union[int, list]]:
    with sqlite3.connect(DB_PATH) as conn:

        try:
            cur = conn.cursor()
            cur.execute(query, params)
        except sqlite3.Error as e:
            print(e)
            context.bot.send_message(chat_id, DB_ERROR)
            return None

        if operation == INSERT:
            conn.commit()
            last_row_id = cur.lastrowid
            return last_row_id

        if operation == DELETE:
            conn.commit()
            return None

        if operation == SELECT:
            rows = cur.fetchall()
            return rows

    return None
