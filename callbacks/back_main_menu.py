from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from callbacks import start
from util.constants import State


def back_main_menu_callback(update:Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    context.user_data[State.START_OVER.value] = True
    start.start_callback(update, context)

    return State.BACK.value