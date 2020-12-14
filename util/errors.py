from telegram import Update
from telegram.ext import CallbackContext
from functools import wraps
import logging


class ValidationError(Exception):

    def __init__(self, details: str, message: str="Missing or Invalid Fields"):
        self.details = details
        self.message = message
        return super().__init__(self.message)


class BackendError(Exception):

    def __init__(self, details: str, message: str="Server error, please try again later"):
        self.details = details
        self.message = message
        return super().__init__(self.message)


def catch_error(f):
    @wraps(f)
    def wrap(update: Update, context: CallbackContext):

        try:
            return f(update, context)
        except ValidationError as e:
            logging.info(f"Client Side Information: {update.message}")
            logging.error(e.details)
            update.message.reply_text(e.message)
        except Exception as e:
            # Add info to error tracking in sentry
            # client.user_context({
            #     "username": update.message.from_user.username,
            #     "message": update.message.text
            # })

            # client.captureException()
            logging.info(f"Client Side Information: {update.message}")
            logging.error(str(e))
            update.message.reply_text("Internal Server Error")

    return wrap


def catch_error_callback_query(f):
    @wraps(f)
    def wrap(update: Update, context: CallbackContext):

        try:
            return f(update, context)
        except ValidationError as e:
            logging.info(f"Client Side Information: {update.message}")
            logging.error(e.details)
            update.callback_query.message.reply_text(e.message)
        except Exception as e:
            # Add info to error tracking in sentry
            # client.user_context({
            #     "username": update.message.from_user.username,
            #     "message": update.message.text
            # })

            # client.captureException()
            logging.info(f"Client Side Information: {update.callback_query}")
            logging.error(str(e))
            update.callback_query.message.reply_text("Internal Server Error")
            

    return wrap