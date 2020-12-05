from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from callbacks import start
import os

load_dotenv()


def main():
    print("Starting.....")
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start.start_callback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()