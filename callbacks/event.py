from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests
from dateutil import parser
from util.enums import State, Constant


def event_callback(update:Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    headers = {"Authorization": "Token " + context.user_data.get("AUTH_TOKEN")}
    response = requests.get("http://127.0.0.1:8000/event", headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        results = response_data["results"]

        keyboard = []
        msg = "*These are the events available for your participation*\n\n"

        for result in results:
            msg += f"{result['eventCode']}:\n"
            msg += f"Name: {result['name']}\n"
            msg += f"Description: {result['description']}\n\n"

            keyboard.append([InlineKeyboardButton(
                result['name'], 
                callback_data=f"{State.EVENT_INSTANCE_LIST.value}={result['eventCode']}"
            )])

        keyboard.append([InlineKeyboardButton("Back", callback_data=str(State.END.value))])
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.answer()
        query.message.reply_text(
            msg, 
            reply_markup=reply_markup, 
            parse_mode='MarkdownV2'
        )

        context.user_data["events"] = results

    return State.EVENT_INSTANCE_LIST.value


def event_instance_callback(update:Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    headers = {"Authorization": "Token " + context.user_data.get("AUTH_TOKEN")}
    eventCode = query.data.split("=")[1]
    response = requests.get("http://127.0.0.1:8000/event/event-instance?eventCode={eventCode}?isCompleted=False", headers=headers)
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
                InlineKeyboardButton("Enroll", callback_data=str(Constant.ENROLL.value)),
                InlineKeyboardButton("Back", callback_data=str(State.END.value))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.answer()
        query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

        return State.ENROLLMENT_SELECTING_ACTION.value


    