from telegram import Update
from telegram.ext import CallbackContext
import requests

def event_callback(update:Update, context: CallbackContext) -> None:

    response = requests.get("http://127.0.0.1:8000/event")
    if response.status_code == 200:
        response_data = response.json()
        results = response_data["results"]

        msg = "*These are the events available for your participation*\n\n"
        for result in results:
            msg += f"/{result['eventCode']}:\n"
            msg += f"Name: {result['name']}\n"
            msg += f"Description: {result['description']}\n\n"

        update.message.reply_text(msg, parse_mode='MarkdownV2')



    