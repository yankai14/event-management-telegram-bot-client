from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests
from dateutil import parser
from util.states import State


def event_instance_callback(update:Update, context: CallbackContext) -> None:

    query = update.callback_query
    eventCode = query.data.split("=")[1]
    response = requests.get("http://127.0.0.1:8000/event/event-instance?eventCode={eventCode}?isCompleted=False")
    if response.status_code == 200:
        responseData = response.json()
        msg = f"*Available slots for {eventCode}*\n\n"
        for eventInstance in responseData:
            
            eventInstanceCode = eventInstance.get("eventInstanceCode")
            location = eventInstance.get("location")
            dates = eventInstance.get("dates")
            fee = eventInstance.get("fee")
            
            msg += f"*Code: {eventInstanceCode}\n*"
            msg += f"Location: {location}\n"
            msg += f"Fees: {fee}\n"
            msg += f"Schedule:\n"

            for count, date in enumerate(dates):
                date = parser.parse(date)
                msg += f"- Session {count}: {date.date()} \({date.date().strftime('%A')}\)\n"

            msg +="\n"
        msg = msg.replace("-", "\-")
        msg = msg.replace(".", "\.")

        keyboard = [
            [
                InlineKeyboardButton("Back", callback_data=str(State.END))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.answer()
        query.edit_message_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
        