from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext


class TelegramService:

    @staticmethod
    def get_query(update: Update):
        query = update if update.message else update.callback_query
        return query

    @staticmethod
    def reply_text(msg: str, update: Update, keyboard: InlineKeyboardMarkup=None):
        query = TelegramService.get_query(update)
        query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=keyboard)

    @staticmethod
    def edit_reply_text(msg: str, update: Update, keyboard: InlineKeyboardMarkup=None):
        query = TelegramService.get_query(update)
        query.message.edit_text(msg, parse_mode='MarkdownV2', reply_markup=keyboard)

    @staticmethod
    def remove_prev_keyboard(update: Update):
        query = TelegramService.get_query(update)
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        