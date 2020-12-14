from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests
from callbacks import start
from util.enums import State, Constant
from util.serializers import RegistrationSerializer
from util.errors import catch_error, catch_error_callback_query, BackendError


@catch_error_callback_query
def register_intro_callback(update:Update, context: CallbackContext) -> None:

    query = update.callback_query

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
            InlineKeyboardButton(text="Done", callback_data=State.REGISTER_SUBMIT.value)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if not context.user_data[State.START_OVER.value]:
        userId = query.from_user["id"]
        try:
            response = requests.get(f"http://127.0.0.1:8000/auth/user?username={userId}")
        except ConnectionError:
            raise ConnectionError("Internal Server Error")
        
        if response.status_code == 200:
            msg = "You are already registered"
            query.edit_message_text(msg, parse_mode='MarkdownV2')
            return State.END.value

        context.user_data["registrationData"] = {Constant.USERNAME.value: userId}
        msg = "Lets get some of the information required"
        query.edit_message_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

    else:
        msg = "Got it\! Please select some feature to update"
        update.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
    
    return State.REGISTER_SELECTING_ACTION.value


@catch_error_callback_query
def prompt_info_callback(update:Update, context: CallbackContext) -> None:

    query = update.callback_query
    feature = Constant(int(query.data)).name.replace("_", " ")
    context.user_data["currentFeature"] = query.data

    if context.user_data["registrationData"].get(int(query.data)):
        msg = f"You are updating *{feature}*, type your *{feature}* here"
    else:
        msg = f"Type your *{feature}*"

    query.answer()
    query.edit_message_text(msg, parse_mode='MarkdownV2')

    return State.REGISTER_GET_INFO.value


@catch_error
def get_info_callback(update:Update, context: CallbackContext) -> None:

    currentFeature = Constant(int(context.user_data["currentFeature"])).value
    context.user_data["registrationData"][currentFeature] = update.message.text

    context.user_data[State.START_OVER.value] = True
    return register_intro_callback(update, context)


@catch_error_callback_query
def submit_info_callback(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    registrationData = context.user_data["registrationData"]
    serializer = RegistrationSerializer()
    payload = serializer.dump(registrationData)
    try:
        response = requests.post("http://127.0.0.1:8000/auth/user", json=payload)
    except ConnectionError:
        raise ConnectionError

    if response.status_code == 201:   
        msg = "Registered"
        query.edit_message_text(msg, parse_mode='MarkdownV2')
        start.start_callback(update, context)
        return State.END.value

    elif response.status_code == 500:
        raise BackendError
        