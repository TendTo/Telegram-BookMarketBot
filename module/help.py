from telegram import Update
from telegram.ext import CallbackContext
from module.shared import HELP_MESSAGE

# pylint: disable=redefined-builtin
def help(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(HELP_MESSAGE, quote=False)
