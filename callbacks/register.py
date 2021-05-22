from http import HTTPStatus
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, user
from telegram.ext import CallbackContext
from callbacks import start
from util.constants import State, Authentication, Other
from util.serializers import RegistrationSerializer
from util.errors import catch_error, BackendError
from util.api_service import ApiService
from util.telegram_service import TelegramService


@catch_error
def register_intro_callback(update:Update, context: CallbackContext) -> None:

    keyboard = [
        [
            InlineKeyboardButton(text="Email", callback_data=Authentication.EMAIL),
            InlineKeyboardButton(text="First Name", callback_data=Authentication.FIRST_NAME),
        ],
        [
            InlineKeyboardButton(text="Last Name", callback_data=Authentication.LAST_NAME),
            InlineKeyboardButton(text="Password", callback_data=Authentication.PASSWORD),
        ],
        [
            InlineKeyboardButton(text="Done", callback_data=State.REGISTER_SUBMIT.value),
            InlineKeyboardButton(text="Back", callback_data=State.END.value)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if not context.user_data.get(State.START_OVER.value):
        TelegramService.remove_prev_keyboard(update)
        user_id = TelegramService.get_user_id(update)

        context.user_data[Authentication.REGISTRATION_DATA] = {
            Authentication.USERNAME: user_id,
            Authentication.PASSWORD: None,
            Authentication.EMAIL: None,
            Authentication.FIRST_NAME: None,
            Authentication.LAST_NAME: None,
            Authentication.PASSWORD: None,
        }

        msg = "Lets get some of the information required"
        TelegramService.edit_reply_text(msg, update, reply_markup)

    else:
        msg = "Got it\! Please select some feature to update"
        TelegramService.reply_text(msg, update, reply_markup)
    
    return State.REGISTER_SELECTING_ACTION.value


def register_prompt_info_callback(update:Update, context: CallbackContext) -> None:

    TelegramService.remove_prev_keyboard(update)
    feature = TelegramService.get_callback_query_data(update)
    context.user_data[Other.CURRENT_FEATURE] = feature

    if context.user_data[Authentication.REGISTRATION_DATA].get(feature):
        msg = f"You are updating *{feature}*, type your *{feature}* here"
    else:
        msg = f"Type your *{feature}*"

    TelegramService.reply_text(msg, update)

    return State.REGISTER_GET_INFO.value


@catch_error
def register_get_info_callback(update:Update, context: CallbackContext) -> None:

    current_feature = context.user_data.get(Other.CURRENT_FEATURE)
    context.user_data[Authentication.REGISTRATION_DATA][current_feature] = update.message.text
    context.user_data[State.START_OVER.value] = True
    return register_intro_callback(update, context)


@catch_error
def register_submit_info_callback(update: Update, context: CallbackContext) -> None:
    
    registration_data = context.user_data[Authentication.REGISTRATION_DATA]
    serializer = RegistrationSerializer()
    payload = serializer.dump(registration_data, register_intro_callback)
    _ ,status_code = ApiService.signup(payload, context)

    if status_code == HTTPStatus.CREATED:
        TelegramService.remove_prev_keyboard(update)
        msg = "Registered, please login to enjoy other features. Returning to main menu...."
        TelegramService.reply_text(msg, update)
        start.start_callback(update, context)
        return State.END.value

    elif status_code == HTTPStatus.BAD_REQUEST:
        TelegramService.remove_prev_keyboard(update)
        msg = "You might have invalid fields, please check your above entries and try again...."
        TelegramService.reply_text(msg, update)
        return register_intro_callback(update, context)

    elif status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        raise BackendError
        