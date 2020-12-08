from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from callbacks import start, event, event_instance
import os
import requests

load_dotenv()


def main():
    print("Starting.....")
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start.start_callback))
    dispatcher.add_handler(CommandHandler("eventlist", event.event_callback))

    response = requests.get("http://127.0.0.1:8000/event")
    if response.status_code == 200:
        response_data = response.json()
        results = response_data["results"]
        for result in results:
            dispatcher.add_handler(CommandHandler(result["eventCode"], event_instance.event_instance_callback))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()