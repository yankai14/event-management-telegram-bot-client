from http import HTTPStatus
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, callbackcontext
from dateutil import parser
from util.errors import catch_error
from util.constants import State, Enrollment, Event, EventInstance
from util.api_service import ApiService
from util.telegram_service import TelegramService
import re


@catch_error
def event_callback(update: Update, context: CallbackContext) -> None:
    
    TelegramService.remove_prev_keyboard(update)
    next_page, previous_page, events, status_code = ApiService.get_event_list(context)
        
    if status_code == HTTPStatus.OK:
        if next_page:
            next_page_section = re.search(r'\?(page=(.+))', next_page)
            next_page_number = next_page_section.group(2)
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
            keyboard.append([InlineKeyboardButton(text="Next Page", callback_data=str(State.EVENT_PAGINATION.value) + ":next_page_number:" + next_page_number)])
            keyboard.append([InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))])
            reply_markup = InlineKeyboardMarkup(keyboard)
            TelegramService.edit_reply_text(msg, update, reply_markup)
            context.user_data[Event.EVENTS] = events

        elif next_page is None:
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

    return State.EVENT_SELECTING_ACTION.value

def event_callback_pagination(update: Update, context: CallbackContext):
    passed_page_section = update.callback_query.data
    passed_page_number = re.search(f'number:(.+)', passed_page_section).group(1)
    next_page, previous_page, events, status_code = ApiService.get_event_list_pagination(
        passed_page_number, context
    )
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

        if next_page and previous_page:
            next_page_section = re.search(r'\?(page=(.+))', next_page)
            next_page_number = next_page_section.group(2)
            previous_page_section = re.search(r'\?(page=(.+))', previous_page)
            previous_page_number = previous_page_section.group(2)
            keyboard.append([
                InlineKeyboardButton(
                text="Previous Page", callback_data=str(State.EVENT_PAGINATION.value) + ":previous_page_number:" + previous_page_number),
                InlineKeyboardButton(
                text="Next Page", callback_data=str(State.EVENT_PAGINATION.value) + ":next_page_number:" + next_page_number)
            ])
            
            keyboard.append([InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))])

            

        elif (next_page) and (previous_page is None):
            next_page_section = re.search(r'\?(page=(.+))', next_page)
            next_page_number = next_page_section.group(2)
            keyboard.append([InlineKeyboardButton(
                text="Next Page", callback_data=str(State.EVENT_PAGINATION.value) + ":next_page_number:" + next_page_number),
            ])
            keyboard.append([InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))])

        elif (next_page is None) and (previous_page):
            previous_page_section = re.search(r'\?(page=(.+))', previous_page)
            previous_page_number = previous_page_section.group(2)
            keyboard.append([InlineKeyboardButton(
                text="Previous Page", callback_data=str(State.EVENT_PAGINATION.value) + ":previous_page_number:" + previous_page_number)
            ])
            keyboard.append([InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))])

        elif (next_page is None) and (previous_page is None):
            keyboard.append([InlineKeyboardButton(text="Back", callback_data=str(State.BACK.value))])

        reply_markup = InlineKeyboardMarkup(keyboard)

        TelegramService.edit_reply_text(msg, update, reply_markup)
        context.user_data[Event.EVENTS] = events

    return State.EVENT_SELECTING_ACTION.value

@catch_error
def event_instance_callback(update:Update, context: CallbackContext) -> None:

    TelegramService.remove_prev_keyboard(update)
    event_code = TelegramService.get_callback_query_data(update).split("=")[1]
    next_page, previous_page, event_instances, status_code = ApiService.get_event_instance_list(event_code, context)

    if event_instances == []:
        msg = "There are no courses for this event currently. Please check back at a later time."
        keyboard = [
            [
                InlineKeyboardButton(text="Back", callback_data=State.EVENT_LIST.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        TelegramService.edit_reply_text(msg, update, reply_markup)

    if (status_code == HTTPStatus.OK) and (event_instances != []):
        if next_page:
            next_page_section = re.search(r'\&(page=(.+))', next_page)
            next_page_number = next_page_section.group(2)
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
                ],
                [
                    InlineKeyboardButton(text="Next Page", callback_data=str(State.EVENT_INSTANCE_PAGINATION.value) + ":next_page_number:" + next_page_number)
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data=State.EVENT_LIST.value)
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            TelegramService.edit_reply_text(msg, update, reply_markup)

        elif next_page is None:
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
                    InlineKeyboardButton(text="Back", callback_data=State.EVENT_LIST.value)
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            TelegramService.edit_reply_text(msg, update, reply_markup)

    return State.ENROLLMENT_SELECTING_ACTION.value

def event_instance_callback_pagination(update:Update, context: CallbackContext) -> None:
    passed_page_section = update.callback_query.data
    passed_page_number = re.search(f'number:(.+)', passed_page_section).group(1)
    event_code_snippet = update.callback_query.message.text
    event_code = re.search(f'slots for (.+)', event_code_snippet).group(1)
    next_page, previous_page, event_instances, status_code = ApiService.get_event_instance_list_pagination(
        passed_page_number, event_code, context
    )
    
    if event_instances == []:
        msg = "There are no courses for this event currently. Please check back at a later time."
        keyboard = [
            [
                InlineKeyboardButton(text="Back", callback_data=State.EVENT_LIST.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        TelegramService.edit_reply_text(msg, update, reply_markup)

    if (status_code == HTTPStatus.OK) and (event_instances != []):
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
        if next_page and previous_page:
            next_page_section = re.search(r'\&(page=(.+))', next_page)
            next_page_number = next_page_section.group(2)
            previous_page_section = re.search(r'\&(page=(.+))', previous_page)
            previous_page_number = previous_page_section.group(2)
            keyboard = [
                [
                    InlineKeyboardButton(text="Enroll", callback_data=Enrollment.ENROLL),
                ],
                [
                    InlineKeyboardButton(text="Previous Page", callback_data=str(State.EVENT_INSTANCE_PAGINATION.value) + ":previous_page_number:" + previous_page_number),
                    InlineKeyboardButton(text="Next Page", callback_data=str(State.EVENT_INSTANCE_PAGINATION.value) + ":next_page_number:" + next_page_number)
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data=State.EVENT_LIST.value)
                ]
            ]

        elif (next_page) and (previous_page is None):
            next_page_section = re.search(r'\&(page=(.+))', next_page)
            next_page_number = next_page_section.group(2)
            keyboard = [
                [
                    InlineKeyboardButton(text="Enroll", callback_data=Enrollment.ENROLL),
                ],
                [
                    InlineKeyboardButton(text="Next Page", callback_data=str(State.EVENT_INSTANCE_PAGINATION.value) + ":next_page_number:" + next_page_number),
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data=State.EVENT_LIST.value)
                ]
            ]

        elif (next_page is None) and (previous_page):
            previous_page_section = re.search(r'\&(page=(.+))', previous_page)
            previous_page_number = previous_page_section.group(2)
            keyboard = [
                [
                    InlineKeyboardButton(text="Enroll", callback_data=Enrollment.ENROLL),
                ],
                [
                    InlineKeyboardButton(text="Previous Page", callback_data=str(State.EVENT_INSTANCE_PAGINATION.value) + ":previous_page_number:" + previous_page_number)
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data=State.EVENT_LIST.value)
                ]
            ]

        elif (next_page is None) and (previous_page is None):
            keyboard = [
                [
                    InlineKeyboardButton(text="Enroll", callback_data=Enrollment.ENROLL),
                ],
                [
                    InlineKeyboardButton(text="Back", callback_data=State.EVENT_LIST.value)
                ]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        TelegramService.edit_reply_text(msg, update, reply_markup)

        return State.ENROLLMENT_SELECTING_ACTION.value