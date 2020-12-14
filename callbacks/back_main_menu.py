from telegram import Update
from telegram.ext import CallbackContext
from callbacks import start
from util.enums import State


def back_main_menu_callback(update:Update, context: CallbackContext) -> None:

    context.user_data[State.START_OVER.value] = True
    start.start_callback(update, context)

    return State.END.value