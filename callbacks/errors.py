from functools import wraps

def catch_error(f):
    @wraps(f)
    def wrap(bot, update):
        #logger.info("User {user} sent {message}".format(user=update.message.from_user.username, message=update.message.text))
        try:
            return f(bot, update)
        except Exception as e:
            # Add info to error tracking
            '''client.user_context({
                "username": update.message.from_user.username,
                "message": update.message.text
            })

            client.captureException()
            logger.error(str(e))'''
            bot.send_message(chat_id=update.message.chat_id,
                             text="An error occured ...")

    return wrap