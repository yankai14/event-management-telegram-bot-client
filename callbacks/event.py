from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import requests
from util.enums import State


def event_callback(update:Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    response = requests.get("http://127.0.0.1:8000/event")
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
        query.message.edit_text(
            msg, 
            reply_markup=reply_markup, 
            parse_mode='MarkdownV2'
        )

        context.user_data["events"] = results

    return State.EVENT_INSTANCE_LIST.value




    