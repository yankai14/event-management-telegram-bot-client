from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from util.enums import State
from util.api_service import ApiService
from util.telegram_service import TelegramService

def start_callback(update:Update, context: CallbackContext) -> None:

    msg = "*Welcome to ALD Event Manager*\n\n"
    msg += "Listed below are the following features you can take advantage of\n"
    msg += "-----------------------------------------\n"
    msg += "Below are the default commands:\n"
    msg += "/start - To start the bot 🏃\n"
    msg += "/stop - To stop the bot✋\n"
    msg += "/report - Report bugs or give feedback👮‍♀️\n"
    msg += "-----------------------------------------\n"
    msg += "Please contact the developer @yankai14 for any queries\n"


    if context.user_data.get("AUTH_TOKEN"):
        keyboard = [
            [
                InlineKeyboardButton(text="Event List", callback_data=str(State.EVENT_LIST.value)),
            ]
        ]

    else:
        userId = TelegramService.get_user_id(update)
        is_registered = ApiService.user_already_registered(userId)
        
        if is_registered:
            keyboard = [
                [
                    InlineKeyboardButton(text="Login", callback_data=str(State.LOGIN.value))
                ]
            ]
        else:
            keyboard = [
                [
                    InlineKeyboardButton(text="Registration", callback_data=str(State.REGISTER.value)),
                ]
            ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    TelegramService.reply_text(msg, update, reply_markup)
    context.user_data[State.START_OVER.value] = False

    return State.FEATURE_SELECTION.value
