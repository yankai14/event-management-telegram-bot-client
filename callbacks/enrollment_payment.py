from os import stat
from callbacks import start
from util.serializers import EnrollmentPaymentSerializer
from util.errors import BackendError, catch_error
from util.api_service import ApiService
from util.telegram_service import TelegramService
from util.constants import EventInstance, Folder, FolderPermission, State, Enrollment, Payment
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, user
from telegram.ext import CallbackContext
from http import HTTPStatus


def enrollment_payment_callback(update:Update, context:CallbackContext):

    msg = "Please click on *event code* if you would like to make payment for a specific event you enrolled for. "

    keyboard = [
        [
            InlineKeyboardButton(text="Event Code", callback_data=Payment.ENROLLMENT_PAYMENT_INFO),
            InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    TelegramService.edit_reply_text(msg, update, reply_markup)
    return State.ENROLLMENT_HISTORY_SELECTING_ACTION.value


def prompt_get_enrolled_info_callback(update:Update, context:CallbackContext):
    TelegramService.remove_prev_keyboard(update)

    msg = "Enter the exact *Event Code* you would like to make payment for"
    TelegramService.edit_reply_text(msg, update)
    return State.ENROLLMENT_PAYMENT_GET_INFO.value

@catch_error
def get_enrolled_info_callback(update:Update, context:CallbackContext):
    event_instance_code = update.message.text 
    username = update["message"]["chat"]["id"]
    enrollment_data = {
        "username": username,
        "eventInstanceCode": event_instance_code
    }
    serializer = EnrollmentPaymentSerializer()
    payload = serializer.dump(enrollment_data)
    response, status_code = ApiService.enrollment_payment(payload, context)
    if response["detail"] != "Not found.":
        if status_code == 200:
            stripe_checkout_url = response["stripe_checkout_url"]
            msg = f"Please proceed to make payment for enrolled course at:\n {stripe_checkout_url}"
            TelegramService.reply_text_with_url(msg, update)

    elif response["detail"] == "Not found.":
        keyboard = [
            [
            InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = "You are not enrolled to any courses at this point of time. Please enroll to a course before makiing payment."
        TelegramService.reply_text(msg, update, reply_markup)

    return State.ENROLLMENT_HISTORY_SELECTING_ACTION.value

    


