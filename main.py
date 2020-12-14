from threading import Event

from telegram.callbackquery import CallbackQuery
from callbacks import stop
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.conversationhandler import ConversationHandler
from callbacks import start, event, event_instance, back_main_menu, register
from util.enums import State, Constant
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

    register_feature_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(register.register_intro_callback, pattern=f"^{str(State.REGISTER.value)}$")],
        states={
            State.REGISTER_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    register.prompt_info_callback, 
                    pattern=f"^{Constant.EMAIL.value}|{Constant.FIRST_NAME.value}|{Constant.LAST_NAME.value}|{Constant.PASSWORD.value}$"
                ),
            ],
            State.REGISTER_GET_INFO.value: [MessageHandler(
                Filters.text & ~Filters.command, 
                register.get_info_callback
            )]
        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                register.submit_info_callback,
                pattern=f"^{State.REGISTER_SUBMIT.value}$"
            )
        ],
        map_to_parent={
            # Return to parent conversation
            State.END.value: State.FEATURE_SELECTION.value
        }
    )

    event_feature_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(event.event_callback, pattern=f"^{State.EVENT_LIST.value}$")],
        states = {
            State.EVENT_INSTANCE_LIST.value: [
                CallbackQueryHandler(
                    event_instance.event_instance_callback,
                    pattern=f"^{State.EVENT_INSTANCE_LIST.value}"
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.END.value)}$"
            ),
            CommandHandler("stop", stop.stop_callback)
        ],
        map_to_parent={
            # Return to parent conversation
            State.END.value: State.FEATURE_SELECTION.value
        }
    )

    feature_selection_handlers = [
        register_feature_conv,
        event_feature_conv,
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start.start_callback)],
        states={
            State.SHOWING.value: [CallbackQueryHandler(start.start_callback, pattern=f"^{str(State.END.value)}$")],
            State.FEATURE_SELECTION.value: feature_selection_handlers,
            State.STOPPING.value: [CommandHandler("stop", stop.stop_callback)],
        },
        fallbacks=[CommandHandler("stop", stop.stop_callback)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()