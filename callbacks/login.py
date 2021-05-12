from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from callbacks import start
from util.errors import catch_error, BackendError
from util.serializers import LoginSerializer
from util.serializers import LoginSerializer
from util.enums import State, Constant
import time
import requests


def login_intro_callback(update: Update, context: CallbackContext) -> None:

    query = update if update.message else update.callback_query

    keyboard = [
            [
                InlineKeyboardButton(text="Password", callback_data=Constant.PASSWORD.value),
            ],
            [
                InlineKeyboardButton(text="Done", callback_data=State.LOGIN_SUBMIT.value),
                InlineKeyboardButton(text="Back", callback_data=State.END.value)
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if not context.user_data.get(State.START_OVER.value):
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        context.user_data["loginData"] = {
            Constant.USERNAME.value: query.from_user["id"]
        }
        msg = "Enter password or return to starting menu"
        query.message.edit_text(msg, reply_markup=reply_markup)
    else:
        msg = "Got it\! Submit or update the password you keyed in"
        query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
        
    return State.LOGIN_SELECTING_ACTION.value


@catch_error
def login_prompt_info_callback(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    feature = Constant(int(query.data)).name.replace("_", " ")
    context.user_data["currentFeature"] = query.data
    
    if context.user_data["loginData"].get(int(query.data)):
        msg = f"You are updating *{feature}*, type your *{feature}* here"
    else:
        msg = f"Type your *{feature}*"
    
    query.answer()
    query.message.reply_text(msg, parse_mode='MarkdownV2')

    return State.LOGIN_GET_INFO.value


@catch_error
def login_get_info_callback(update: Update, context: CallbackContext) -> None:

    currentFeature = Constant(int(context.user_data["currentFeature"])).value
    context.user_data["loginData"][currentFeature] = update.message.text
    context.user_data[State.START_OVER.value] = True
    return login_intro_callback(update, context)


@catch_error
def login_submit_info_callback(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    loginData = context.user_data["loginData"]
    serializer = LoginSerializer()
    payload = serializer.dump(loginData)

    response = requests.post("http://127.0.0.1:8000/auth/login", json=payload)

    if response.status_code == 200:   
        context.user_data["AUTH_TOKEN"] = response.json()["token"]
        msg = "Logged In, returning to main menu\.\.\.\."
        context.user_data.pop("loginData", None)
        context.user_data.pop("currentFeature", None)
        query.message.reply_text(msg, parse_mode='MarkdownV2')
        start.start_callback(update, context)
        return State.END.value

    elif response.status_code == 400:
        msg = "Unsuccessful login, please try again"
        context.user_data.pop(State.START_OVER.value, None)
        keyboard = [
            [
                InlineKeyboardButton(text="Try Again", callback_data=State.START_OVER.value),
                InlineKeyboardButton(text="Main Menu", callback_data=State.END.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

        return State.LOGIN_SELECTING_ACTION.value

    else:
        raise BackendError


@catch_error
def login_back__to_intro_callback(update: Update, context: CallbackContext) -> None:
    
    context.user_data[State.START_OVER.value] = True
    return login_intro_callback(update, context)