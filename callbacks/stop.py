from telegram import Update
from telegram.ext import CallbackContext
from util.enums import State

def stop_callback(update: Update, context: CallbackContext) -> None:
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')
    return State.END.value
