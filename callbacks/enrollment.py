from callbacks import start
from util.serializers import EnrollmentSerializer
from util.enums import State, Constant
from util.errors import BackendError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests
import time


def enrollment_prompt_info_callback(update:Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))

    msg = "Enter the exact *Event Schedule Code* that you want to enroll for here"
    query.message.reply_text(msg, parse_mode="MarkdownV2")

    return State.ENROLLMENT_GET_INFO.value
    

def enrollment_get_info_callback(update:Update, context: CallbackContext) -> None:

    eventInstanceCode = update.message.text
    headers = {"Authorization": "Token " + context.user_data.get("AUTH_TOKEN")}
    response = requests.get(f"http://127.0.0.1:8000/event-instance/{eventInstanceCode}", headers=headers)
    if response.status_code == 200:
        eventInstance = response.json()
        context.user_data["enrollmentData"] = eventInstance
        context.user_data["enrollmentData"]["username"] = update.message.from_user["id"]
        context.user_data["enrollmentData"]["role"] = 1
        msg = "To confirm your enrollment, click on the *enroll* button below"
        keyboard = [
            [
                InlineKeyboardButton(text="Confirm", callback_data=Constant.CHECKOUT.value),
            ],
            [
                InlineKeyboardButton(text="Update", callback_data=State.START_OVER.value),
                InlineKeyboardButton(text="Back", callback_data=State.END.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(msg, parse_mode="MarkdownV2", reply_markup=reply_markup)
        return State.ENROLLMENT_SUBMIT.value

    elif response.status_code == 404:
        msg = "Invalid code, please click *Update* to re-enter or *Back* to return to main menu"
        keyboard = [
            [
                InlineKeyboardButton(text="Update", callback_data=State.START_OVER.value),
                InlineKeyboardButton(text="Back", callback_data=State.END.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(msg, parse_mode="MarkdownV2", reply_markup=reply_markup)


def enrollment_submit_info_callback(update:Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    enrollmentData = context.user_data["enrollmentData"]
    serializer = EnrollmentSerializer()
    payload = serializer.dump(enrollmentData)

    headers = {"Authorization": "Token " + context.user_data.get("AUTH_TOKEN")}
    enrollmentExist = requests.get(f"http://127.0.0.1:8000/enrollment?username={", headers=headers)

    response = requests.post("http://127.0.0.1:8000/enrollment", json=payload, headers=headers)

    if response.status_code == 201:   
        msg = "Enrolled to course, returning to main menu\.\.\.\."
        context.user_data[State.START_OVER.value] = True
        context.user_data.pop("enrollmentData", None)
        time.sleep(1.5)
        query.message.reply_text(msg, parse_mode='MarkdownV2')
        start.start_callback(update, context)
        return State.END.value

    elif response.status_code == 409:
        msg = "User is already enrolled\.\.\.\."
        context.user_data[State.START_OVER.value] = True
        context.user_data.pop("enrollmentData", None)
        time.sleep(1.5)
        query.message.reply_text(msg, parse_mode='MarkdownV2')
        start.start_callback(update, context)
        return State.END.value

    else:
        BackendError(details=response.status_code)