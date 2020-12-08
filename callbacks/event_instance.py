from telegram import Update
from telegram.ext import CallbackContext
import requests
from dateutil import parser

def event_instance_callback(update:Update, context: CallbackContext) -> None:

    eventCode = update.message.text.strip(" /")
    response = requests.get("http://127.0.0.1:8000/event/event-instance?eventCode={eventCode}?isCompleted=False")
    if response.status_code == 200:
        responseData = response.json()
        msg = f"*Available slots for {eventCode}*\n\n"
        for eventInstance in responseData:
            
            eventInstanceCode = eventInstance.get("eventInstanceCode")
            location = eventInstance.get("location")
            dates = eventInstance.get("dates")
            
            msg += f"*Code: {eventInstanceCode}\n*"
            msg += f"Location: {location}\n"
            msg += f"Schedule:\n"

            for count, date in enumerate(dates):
                date = parser.parse(date)
                msg += f"- Session {count}: {date.date()} \({date.date().strftime('%A')}\)\n"

            msg +="\n"
        msg = msg.replace("-", "/")
        

    update.message.reply_text(msg, parse_mode='MarkdownV2')




        