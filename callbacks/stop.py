from telegram import Update
from telegram.ext import CallbackContext
from util.enums import State

def stop_callback(update: Update, context: CallbackContext) -> None:
    """End Conversation by command."""
    if "AUTH_TOKEN" in context.user_data.keys():
        del context.user_data["AUTH_TOKEN"]
    update.message.reply_text('Okay, bye.')
    return State.END.value
