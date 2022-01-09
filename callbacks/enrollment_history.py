from http import HTTPStatus
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from util.errors import catch_error
from util.api_service import ApiEndpoints, ApiService
from util.telegram_service import TelegramService
from util.constants import EventInstance, State, History, Payment
from util.constants import Enrollment
from datetime import datetime
import re


def history_callback(update: Update, context: CallbackContext) -> None:

    TelegramService.remove_prev_keyboard(update)   
    next_page, previous_page, enrollments, status_code = ApiService.get_user_enrollments(
        TelegramService.get_user_id(update), context
    )

    if next_page:
        next_page_section = re.search(r'\?(page=(.+))&', next_page)
        next_page_number = next_page_section.group(2)

    if previous_page:
        previous_page_section = re.search(r'\?(page=(.+))&', previous_page)
        previous_page_number = previous_page_section.group(2)

    if status_code == HTTPStatus.OK and len(enrollments) > 0:
        msg = "*These are the events instances you are enrolled in*\n\n"

        for id, enrollment in enumerate(enrollments):
            msg += f"*{id+1}: {enrollment[History.EVENT_INSTANCE][EventInstance.CODE]}*\n"
            msg += f"Location: {enrollment[History.EVENT_INSTANCE][EventInstance.LOCATION]}\n"
            msg += f"Application role: {Enrollment.ROLE_ENUM(enrollment[Enrollment.ROLE]).name}\n"
            msg += f"Completed: {enrollment[History.EVENT_INSTANCE][EventInstance.IS_COMPLETED]}\n\n"

        if next_page:
            keyboard = [
                [
                    InlineKeyboardButton(
                        text="Next Page", callback_data=str(State.ENROLLMENT_HISTORY_PAGINATION.value) + ":next_page_number:" + next_page_number)
                ],
                [
                    InlineKeyboardButton(
                        text="More info", callback_data=History.ENROLLMENT_INFO),
                    InlineKeyboardButton(
                        text="Back", callback_data=str(State.BACK.value))
                ]
            ]

        elif next_page is None:
            keyboard = [
                [
                    InlineKeyboardButton(
                        text="More info", callback_data=History.ENROLLMENT_INFO),
                    InlineKeyboardButton(
                        text="Back", callback_data=str(State.BACK.value))
                ]
            ] 
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        TelegramService.edit_reply_text(msg, update, reply_markup)

    if status_code == HTTPStatus.OK and len(enrollments) == 0:
        msg = "You havent enrolled to any event instances yet"
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Back", callback_data=str(State.BACK.value))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        TelegramService.edit_reply_text(msg, update, reply_markup)

    return State.ENROLLMENT_HISTORY_SELECTING_ACTION.value

def history_callback_pagination(update: Update, context: CallbackContext):
    passed_page_section = update.callback_query.data
    passed_page_number = re.search(f'number:(.+)', passed_page_section).group(1)
    next_page, previous_page, enrollments, status_code = ApiService.get_user_enrollments_pagination(
        TelegramService.get_user_id(update), passed_page_number, context
    )

    if status_code == HTTPStatus.OK and len(enrollments) > 0:
        msg = "*These are the events instances you are enrolled in*\n\n"

        for id, enrollment in enumerate(enrollments):
            msg += f"*{id+1}: {enrollment[History.EVENT_INSTANCE][EventInstance.CODE]}*\n"
            msg += f"Location: {enrollment[History.EVENT_INSTANCE][EventInstance.LOCATION]}\n"
            msg += f"Application role: {Enrollment.ROLE_ENUM(enrollment[Enrollment.ROLE]).name}\n"
            msg += f"Completed: {enrollment[History.EVENT_INSTANCE][EventInstance.IS_COMPLETED]}\n\n"

        if next_page and previous_page:
            next_page_section = re.search(r'\?(page=(.+))&', next_page)
            next_page_number = next_page_section.group(2)
            previous_page_section = re.search(r'\?(page=(.+))&', previous_page)
            previous_page_number = previous_page_section.group(2)
            keyboard = [
                [
                    InlineKeyboardButton(
                        text="Previous Page", callback_data=str(State.ENROLLMENT_HISTORY_PAGINATION.value) + ":previous_page_number:" + previous_page_number),
                    InlineKeyboardButton(
                        text="Next Page", callback_data=str(State.ENROLLMENT_HISTORY_PAGINATION.value) + ":next_page_number:" + next_page_number)
                ],
                [
                    InlineKeyboardButton(
                        text="More info", callback_data=History.ENROLLMENT_INFO),
                    InlineKeyboardButton(
                        text="Back", callback_data=str(State.BACK.value))
                ]
            ]
        elif (next_page) and (previous_page is None):
            next_page_section = re.search(r'\?(page=(.+))&', next_page)
            next_page_number = next_page_section.group(2)
            keyboard = [
                [
                    InlineKeyboardButton(
                        text="Next Page", callback_data=str(State.ENROLLMENT_HISTORY_PAGINATION.value) + ":next_page_number:" + next_page_number)
                ],
                [
                    InlineKeyboardButton(
                        text="More info", callback_data=History.ENROLLMENT_INFO),
                    InlineKeyboardButton(
                        text="Back", callback_data=str(State.BACK.value))
                ]
            ]
        elif (next_page is None) and (previous_page):
            previous_page_section = re.search(r'\?(page=(.+))&', previous_page)
            previous_page_number = previous_page_section.group(2)
            keyboard = [
                [
                    InlineKeyboardButton(
                        text="Previous Page",callback_data=str(State.ENROLLMENT_HISTORY_PAGINATION.value) + ":previous_page_number:" + previous_page_number),
                ],
                [
                    InlineKeyboardButton(
                        text="More info", callback_data=History.ENROLLMENT_INFO),
                    InlineKeyboardButton(
                        text="Back", callback_data=str(State.BACK.value))
                ]
            ]
        elif (next_page is None) and (previous_page is None):
            keyboard = [
                [
                    InlineKeyboardButton(
                        text="More info", callback_data=History.ENROLLMENT_INFO),
                    InlineKeyboardButton(
                        text="Back", callback_data=str(State.BACK.value))
                ]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        TelegramService.edit_reply_text(msg, update, reply_markup)

    return State.ENROLLMENT_HISTORY_SELECTING_ACTION.value
    


def history_prompt_info_callback(update: Update, context: CallbackContext):
    TelegramService.remove_prev_keyboard(update)

    msg = "Enter the exact *Event Instance Code* that you are enrolled"
    TelegramService.reply_text(msg, update)

    return State.ENROLLMENT_GET_INFO.value


def history_get_info_callback(update: Update, context: CallbackContext):

    event_instance_code = update.message.text
    enrollment, status_code = ApiService.get_specific_enrollment(
        TelegramService.get_user_id(update), event_instance_code, context
    )

    if status_code == HTTPStatus.OK and enrollment:
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Get Another Enrollment Info", callback_data=History.ENROLLMENT_INFO),
                InlineKeyboardButton(
                    text="Back", callback_data=str(State.BACK.value))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = f"*{enrollment[History.EVENT_INSTANCE][EventInstance.CODE]}* 🙌\n"
        msg += f"-----------------------------------------------\n"
        msg += f"Event 🎟️: {enrollment[History.EVENT_INSTANCE][EventInstance.EVENT]}\n"
        msg += f"Location 📍: {enrollment[History.EVENT_INSTANCE][EventInstance.LOCATION]}\n"
        msg += f"-----------------------------------------------\n"
        msg += f"Dates 📅:\n"
        dates = enrollment[History.EVENT_INSTANCE][EventInstance.DATES]
        for date in dates:
            dt = datetime.strptime(
                date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%c")
            msg += f"- {dt}\n"
        msg += f"-----------------------------------------------\n"
        msg += f"Application status 📖: {Enrollment.STATUS_ENUM(enrollment[Enrollment.STATUS]).name}\n"
        msg += f"Payment Id: {enrollment[Payment.PAYMENT_ID]}\n"
        msg += f"Application role 😊: {Enrollment.ROLE_ENUM(enrollment[Enrollment.ROLE]).name}\n"
        msg += f"Is completed ✅: {enrollment[History.EVENT_INSTANCE][EventInstance.IS_COMPLETED]}\n"
        TelegramService.reply_text(msg, update, reply_markup)
        return State.ENROLLMENT_HISTORY_SELECTING_ACTION.value

    elif not enrollment:
        msg = "No such enrollment, please re-enter the exact *Event Instance Code* that you are enrolled"
        TelegramService.reply_text(msg, update)