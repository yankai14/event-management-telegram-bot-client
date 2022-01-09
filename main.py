from callbacks import stop
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.conversationhandler import ConversationHandler
from callbacks import (
    start,
    event,
    enrollment,
    back_main_menu,
    register,
    login,
    enrollment_history,
    enrollment_payment
)
from util.enums import Constant
from util.constants import Enrollment, History, State, Authentication, Payment
from util.config import ENV
import os
import logging

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def main():
    updater = Updater(token=ENV.TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    register_feature_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            register.register_intro_callback, pattern=f"^{str(State.REGISTER.value)}$")],
        states={
            State.REGISTER_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    register.register_prompt_info_callback,
                    pattern=f"^{Authentication.EMAIL}|{Authentication.FIRST_NAME}|{Authentication.LAST_NAME}|{Authentication.PASSWORD}$"
                ),
            ],
            State.REGISTER_GET_INFO.value: [MessageHandler(
                Filters.text & ~Filters.command,
                register.register_get_info_callback
            )]
        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.BACK.value)}$"
            ),
            CallbackQueryHandler(
                register.register_submit_info_callback,
                pattern=f"^{State.REGISTER_SUBMIT.value}$"
            )
        ],
        map_to_parent={
            # Return to parent conversation
            State.BACK.value: State.FEATURE_SELECTION.value,
            State.END.value: State.END.value
        }
    )

    login_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(
            login.login_intro_callback, pattern=f"^{str(State.LOGIN.value)}")],
        states={
            State.LOGIN_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    login.login_prompt_info_callback,
                    pattern=f"^{Authentication.PASSWORD}$"
                )
            ],
            State.LOGIN_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    login.login_get_info_callback
                )
            ]
        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.BACK.value)}$"
            ),
            CallbackQueryHandler(
                login.login_intro_callback,
                pattern=f"^{str(State.START_OVER.value)}$"
            ),
            CallbackQueryHandler(
                login.login_submit_info_callback,
                pattern=f"^{State.LOGIN_SUBMIT.value}$"
            )
        ],
        map_to_parent={
            # Return to parent conversation
            State.BACK.value: State.FEATURE_SELECTION.value,
            State.END.value: State.END.value
        }
    )

    enrollment_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                enrollment.enrollment_prompt_info_callback,
                pattern=f"^{Enrollment.ENROLL}$"
            )
        ],
        states={
            State.ENROLLMENT_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    enrollment.enrollment_get_info_callback
                )
            ],
            State.ENROLLMENT_SELECT_ROLE.value: [
                CallbackQueryHandler(
                    enrollment.enrollment_set_role_callback,
                    pattern=f"^{Enrollment.ROLE_ENUM.PARTICIPANT.value}|{Enrollment.ROLE_ENUM.FACILITATOR.value}$"
                )
            ],
            State.ENROLLMENT_SUBMIT.value: [
                CallbackQueryHandler(
                    enrollment.enrollment_submit_info_callback,
                    pattern=f"^{Enrollment.CHECKOUT}$"
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                enrollment.enrollment_prompt_info_callback,
                pattern=f"^{State.START_OVER.value}$"
            ),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{State.BACK.value}$"
            ),
            CommandHandler("stop", stop.stop_callback)
        ],
        map_to_parent={
            # Return to parent conversation
            State.BACK.value: State.BACK.value,
            State.END.value: State.END.value
        }
    )
    
    event_feature_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                event.event_callback,
                pattern=f"^{State.EVENT_LIST.value}$"
            )
        ],
        states={
            State.EVENT_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    event.event_callback_pagination,
                    pattern=f"^{str(State.EVENT_PAGINATION.value)}"
                ),
                CallbackQueryHandler(
                    event.event_instance_callback,
                    pattern=f"^{State.EVENT_INSTANCE_LIST.value}"
                )
            ],
            State.ENROLLMENT_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    event.event_callback,
                    pattern=f"^{State.EVENT_LIST.value}$"
                ),
                CallbackQueryHandler(
                    event.event_instance_callback_pagination,
                    pattern=f"^{State.EVENT_INSTANCE_PAGINATION.value}"
                ),
                enrollment_conv],
        },
        fallbacks=[
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{State.BACK.value}$"
            ),
            CommandHandler("stop", stop.stop_callback)
        ],
        map_to_parent={
            # Return to parent conversation
            State.BACK.value: State.FEATURE_SELECTION.value,
            State.END.value: State.END.value
        }
    )
    

    enrollment_payment_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                enrollment_payment.enrollment_payment_callback,
                pattern=f"^{State.ENROLLMENT_PAYMENT.value}$"
            )
        ],
        states={
            State.ENROLLMENT_HISTORY_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    enrollment_payment.prompt_get_enrolled_info_callback,
                    pattern=f"^{Payment.ENROLLMENT_PAYMENT_INFO}$"
                )
            ],
            State.ENROLLMENT_PAYMENT_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    enrollment_payment.get_enrolled_info_callback
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{State.BACK.value}$"
            ),
            CommandHandler("stop", stop.stop_callback)
        ],
        map_to_parent={
            # Return to parent conversation
            State.BACK.value: State.FEATURE_SELECTION.value,
            State.END.value: State.END.value
        }        
    )


    enrollment_history_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                enrollment_history.history_callback,
                pattern=f"^{State.ENROLLMENT_HISTORY.value}$"
            )
        ],
        states={
            State.ENROLLMENT_HISTORY_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    enrollment_history.history_prompt_info_callback,
                    pattern=f"^{History.ENROLLMENT_INFO}"),
                CallbackQueryHandler(
                    enrollment_history.history_callback_pagination,
                    pattern=f"^{State.ENROLLMENT_HISTORY_PAGINATION.value}"
                )
            ],
            State.ENROLLMENT_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    enrollment_history.history_get_info_callback
                )
            ]
        },
        fallbacks=[
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{State.BACK.value}$"
            ), 
            CommandHandler("stop", stop.stop_callback)
        ],
        map_to_parent={
            # Return to parent conversation
            State.BACK.value: State.FEATURE_SELECTION.value,
            State.END.value: State.END.value
        }
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start.start_callback)],
        states={
            State.SHOWING.value: [CallbackQueryHandler(start.start_callback, pattern=f"^{str(State.BACK.value)}$")],
            State.FEATURE_SELECTION.value: [
                register_feature_conv,
                login_conv_handler,
                event_feature_conv,
                enrollment_history_conv,
                enrollment_payment_conv
            ],
            State.STOPPING.value: [CommandHandler("stop", stop.stop_callback)],
        },
        fallbacks=[CommandHandler("stop", stop.stop_callback)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
