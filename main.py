from threading import Event
from callbacks import stop
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.conversationhandler import ConversationHandler
from callbacks import start, event, event_instance, back_main_menu
from util.states import State
import os
import logging

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def main():

    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher

    event_feature_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(event.event_callback)],
        states = {
            State.EVENT_INSTANCE_LIST: [
                CallbackQueryHandler(
                    event_instance.event_instance_callback,
                    pattern=f"^{State.EVENT_INSTANCE_LIST}"
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.END)}$"
            ),
            CommandHandler("stop", stop.stop_callback)
        ],
        map_to_parent={
            # Return to parent conversation
            State.END: State.FEATURE_SELECTION
        }
    )

    feature_selection_handlers = [
        event_feature_conv,
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start.start_callback)],
        states={
            State.SHOWING: [CallbackQueryHandler(start.start_callback, pattern=f"^{str(State.END)}$")],
            State.FEATURE_SELECTION: feature_selection_handlers,
            State.STOPPING: [CommandHandler("stop", stop.stop_callback)],
        },
        fallbacks=[CommandHandler("stop", stop.stop_callback)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()