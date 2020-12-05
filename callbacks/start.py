from telegram import Update
from telegram.ext import CallbackContext


def start_callback(update:Update, context: CallbackContext) -> None:

    msg = "*Welcome to ALD Event Manager*\n\n"
    msg += "Listed below are the following commands:\n"
    msg += "/eventlist\n"
    msg += "/registration\n"

    update.message.reply_text(msg, parse_mode='MarkdownV2')