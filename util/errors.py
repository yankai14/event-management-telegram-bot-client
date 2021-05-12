from types import FunctionType
from telegram import Update
from telegram.ext import CallbackContext
from functools import wraps
from util.enums import State
import logging

class ValidationError(Exception):

    def __init__(self, details: str, message: str="Missing or Invalid Fields", callback: FunctionType = None):
        self.details = details
        self.message = message
        self.callback = callback
        return super().__init__(self.message)


class BackendError(Exception):

    def __init__(self, details: str, message: str="Server error, please try again later"):
        self.details = details
        self.message = message
        return super().__init__(self.message)


def catch_error(f):
    @wraps(f)
    def wrap(update: Update, context: CallbackContext):

        query = update if update.message else update.callback_query

        try:
            return f(update, context)
        except ValidationError as e:
            logging.info(f"Client Side Information: {update.message}")
            logging.error(e.details)
            query.message.edit_text(e.message)
            context.user_data[State.START_OVER.value] = True
            if e.callback:
                e.callback(update, context)
        except Exception as e:
            logging.info(f"Client Side Information: {update.message}")
            logging.error(str(e))
            query.message.reply_text("Internal Server Error")

    return wrap