from telegram import Update
from telegram.ext import CallbackContext
from module.shared import START_MESSAGE


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(START_MESSAGE, quote=False)
