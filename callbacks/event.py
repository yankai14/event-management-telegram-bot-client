from http import HTTPStatus
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from dateutil import parser
from util.errors import catch_error
from util.constants import State, Enrollment, Event, EventInstance
from util.api_service import ApiService
from util.telegram_service import TelegramService


@catch_error
def event_callback(update:Update, context: CallbackContext) -> None:

    TelegramService.remove_prev_keyboard(update)
    events, status_code = ApiService.get_event_list(context)
    if status_code == HTTPStatus.OK:
        keyboard = []
        msg = "*These are the events available for your participation*\n\n"

        for event in events:
            msg += f"{event[Event.CODE]}:\n"
            msg += f"Name: {event[Event.NAME]}\n"
            msg += f"Description: {event[Event.DESCRIPTION]}\n\n"
            keyboard.append([InlineKeyboardButton(
                text=event[Event.NAME], 
                callback_data=f"{State.EVENT_INSTANCE_LIST.value}={event[Event.CODE]}"
            )])

        keyboard.append([InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))])
        reply_markup = InlineKeyboardMarkup(keyboard)

        TelegramService.edit_reply_text(msg, update, reply_markup)
        context.user_data[Event.EVENTS] = events
    #TODO: Handle HTTPStatus 500 and 400

    return State.EVENT_INSTANCE_LIST.value


@catch_error
def event_instance_callback(update:Update, context: CallbackContext) -> None:

    TelegramService.remove_prev_keyboard(update)
    event_code = TelegramService.get_callback_query_data(update).split("=")[1]
    event_instances, status_code = ApiService.get_event_instance_list(event_code, context)
    if status_code == HTTPStatus.OK:

        # Add scenario where there is no eventInstanceCode created for particular eventCode yet
        if event_instances == []:
            msg = "*No event slots created yet*"
            keyboard = [
                [InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            TelegramService.edit_reply_text(msg, update, reply_markup)
            return State.ENROLLMENT_SELECTING_ACTION.value
            
        msg = f"*Available slots for {event_code}*\n\n"
        for event_instance in event_instances:
            event_instance_code = event_instance.get(EventInstance.CODE)
            location = event_instance.get(EventInstance.LOCATION)
            dates = event_instance.get(EventInstance.DATES)
            fee = event_instance.get(EventInstance.FEE)
            msg += f"*Code: {event_instance_code}\n*"
            msg += f"Location: {location}\n"
            msg += f"Fees: {fee}\n"
            msg += f"Schedule:\n"
            for count, date in enumerate(dates):
                date = parser.parse(date)
                msg += f"- Session {count}: {date.date()} \({date.date().strftime('%A')}\)\n"

            msg +="\n"
        keyboard = [
            [
                InlineKeyboardButton(text="Enroll", callback_data=Enrollment.ENROLL),
                InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        TelegramService.edit_reply_text(msg, update, reply_markup)

        return State.ENROLLMENT_SELECTING_ACTION.value




