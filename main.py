from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.conversationhandler import ConversationHandler
from callbacks import start, event, event_instance
from util.conv_flow.payment_flow import PaymentFlow
import os


load_dotenv()


def main():
    print("Starting.....")
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start.start_callback))

    payment_flow = ConversationHandler(
        entry_points=[CommandHandler("eventlist", event.event_callback)],
        states={
            PaymentFlow.EVENT_INSTANCE: [CallbackQueryHandler(event_instance.event_instance_callback)],
        },
        fallbacks=[CommandHandler("eventlist", event.event_callback)]
    )

    dispatcher.add_handler(payment_flow)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()