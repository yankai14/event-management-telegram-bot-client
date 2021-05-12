from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests
from callbacks import start
from util.enums import State, Constant
from util.serializers import RegistrationSerializer
from util.errors import catch_error, BackendError
import time


def register_intro_callback(update:Update, context: CallbackContext) -> None:

    keyboard = [
        [
            InlineKeyboardButton(text="Email", callback_data=Constant.EMAIL.value),
            InlineKeyboardButton(text="First Name", callback_data=Constant.FIRST_NAME.value),
        ],
        [
            InlineKeyboardButton(text="Last Name", callback_data=Constant.LAST_NAME.value),
            InlineKeyboardButton(text="Password", callback_data=Constant.PASSWORD.value),
        ],
        [
            InlineKeyboardButton(text="Done", callback_data=State.REGISTER_SUBMIT.value),
            InlineKeyboardButton(text="Back", callback_data=State.END.value)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query = update if update.message else update.callback_query

    if not context.user_data[State.START_OVER.value]:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        userId = query.from_user["id"]
        response = requests.get(f"http://127.0.0.1:8000/auth/user/{userId}")
        
        if response.status_code == 200:
            context.user_data[State.START_OVER.value] = False
            msg = "You are already registered, returning to main menu\.\.\.\."
            query.message.reply_text(msg, parse_mode='MarkdownV2')
            time.sleep(1)
            start.start_callback(update, context)
            return State.END.value

        context.user_data["registrationData"] = {Constant.USERNAME.value: userId}
        msg = "Lets get some of the information required"
        query.message.edit_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

    else:
        msg = "Got it\! Please select some feature to update"
        query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
    
    return State.REGISTER_SELECTING_ACTION.value


@catch_error
def register_prompt_info_callback(update:Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    feature = Constant(int(query.data)).name.replace("_", " ")
    context.user_data["currentFeature"] = query.data

    if context.user_data["registrationData"].get(int(query.data)):
        msg = f"You are updating *{feature}*, type your *{feature}* here"
    else:
        msg = f"Type your *{feature}*"

    query.answer()
    query.message.reply_text(msg, parse_mode='MarkdownV2')

    return State.REGISTER_GET_INFO.value


@catch_error
def register_get_info_callback(update:Update, context: CallbackContext) -> None:

    currentFeature = Constant(int(context.user_data["currentFeature"])).value
    context.user_data["registrationData"][currentFeature] = update.message.text

    context.user_data[State.START_OVER.value] = True
    return register_intro_callback(update, context)


@catch_error
def register_submit_info_callback(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    registrationData = context.user_data["registrationData"]
    serializer = RegistrationSerializer()
    payload = serializer.dump(registrationData, register_intro_callback)
    response = requests.post("http://127.0.0.1:8000/auth/user", json=payload)

    if response.status_code == 201:
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        msg = "Registered, please login to enjoy other features\. Returning to main menu\.\.\.\."
        del context.user_data["registrationData"]
        del context.user_data["currentFeature"]
        query.message.reply_text(msg, parse_mode='MarkdownV2')
        start.start_callback(update, context)
        return State.END.value

    elif response.status_code == 500:
        raise BackendError
        