from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from util.states import State


def start_callback(update:Update, context: CallbackContext) -> None:

    msg = "*Welcome to ALD Event Manager*\n\n"
    msg += "Listed below are the following features you can take advantage of:\n"
    msg += "Type /stop to exit the bot"
    
    keyboard = [
        [
            InlineKeyboardButton(text="Event List", callback_data=str(State.EVENT_LIST)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.user_data.get(State.START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
    else:
        update.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

    context.user_data[State.START_OVER] = False
    return State.FEATURE_SELECTION
