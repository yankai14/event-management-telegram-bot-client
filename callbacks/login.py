from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from callbacks import start
from http import HTTPStatus
from util.errors import catch_error, BackendError
from util.serializers import LoginSerializer
from util.serializers import LoginSerializer
from util.constants import State, Authentication, Other
from util.api_service import ApiService
from util.telegram_service import TelegramService


@catch_error
def login_intro_callback(update: Update, context: CallbackContext) -> None:

    keyboard = [
            [
                InlineKeyboardButton(text="Password", callback_data=Authentication.PASSWORD),
            ],
            [
                InlineKeyboardButton(text="Done", callback_data=State.LOGIN_SUBMIT.value),
                InlineKeyboardButton(text="Back", callback_data=State.BACK.value)
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if not context.user_data.get(State.START_OVER.value):
        TelegramService.remove_prev_keyboard(update)
        user_id = TelegramService.get_user_id(update)

        context.user_data[Authentication.LOGIN_DATA] = {
            Authentication.USERNAME: user_id,
            Authentication.PASSWORD: None
        }

        msg = "Enter password or return to starting menu"
        TelegramService.edit_reply_text(msg, update, reply_markup)
    else:
        msg = "Submit or update the password you keyed in"
        TelegramService.reply_text(msg, update, reply_markup)
        
    return State.LOGIN_SELECTING_ACTION.value


@catch_error
def login_prompt_info_callback(update: Update, context: CallbackContext) -> None:

    TelegramService.remove_prev_keyboard(update)
    feature = TelegramService.get_callback_query_data(update)
    context.user_data[Other.CURRENT_FEATURE] = feature
    
    if context.user_data[Authentication.LOGIN_DATA].get(feature):
        msg = f"You are updating *{feature}*, type your *{feature}* here"
    else:
        msg = f"Type your *{feature}*"
    
    TelegramService.edit_reply_text(msg, update)

    return State.LOGIN_GET_INFO.value


@catch_error
def login_get_info_callback(update: Update, context: CallbackContext) -> None:

    current_feature = context.user_data.get(Other.CURRENT_FEATURE)
    context.user_data[Authentication.LOGIN_DATA][current_feature] = update.message.text
    context.user_data[State.START_OVER.value] = True
    return login_intro_callback(update, context)


@catch_error
def login_submit_info_callback(update: Update, context: CallbackContext) -> None:

    login_data = context.user_data[Authentication.LOGIN_DATA]
    serializer = LoginSerializer()
    payload = serializer.dump(login_data, login_intro_callback)
    _ ,status_code = ApiService.login(payload, context)

    if status_code == HTTPStatus.OK:
        TelegramService.remove_prev_keyboard(update)
        msg = "Logged In, returning to main menu...."
        TelegramService.edit_reply_text(msg, update)
        start.start_callback(update, context)
        return State.BACK.value

    elif status_code == 400:
        TelegramService.remove_prev_keyboard(update)
        msg = "Unsuccessful login, please try again"
        TelegramService.reply_text(msg, update)
        return login_intro_callback(update, context)

    else:
        raise BackendError