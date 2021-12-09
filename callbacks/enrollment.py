from callbacks import start
from util.serializers import EnrollmentSerializer
from util.errors import BackendError, catch_error
from util.api_service import ApiService
from util.telegram_service import TelegramService
from util.constants import EventInstance, Folder, FolderPermission, State, Enrollment
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from http import HTTPStatus


@catch_error
def enrollment_prompt_info_callback(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))

    msg = "Enter the exact *Event Schedule Code* that you want to enroll for here"
    query.message.reply_text(msg, parse_mode="MarkdownV2")

    return State.ENROLLMENT_GET_INFO.value


def enrollment_get_info_callback(update: Update, context: CallbackContext) -> None:

    event_instance_code = update.message.text
    event_instance, status_code = ApiService.get_specific_event_instance(
        event_instance_code, context)
    # if status_code == HTTPStatus.OK and event_instance.get(EventInstance.IS_COMPLETED):
    if status_code == HTTPStatus.OK:        

        context.user_data[Enrollment.ENROLLMENT_DATA] = {
            Enrollment.USERNAME: TelegramService.get_user_id(update),
            Enrollment.ROLE: Enrollment.ROLE_ENUM.PARTICIPANT.value,
            Enrollment.STATUS: Enrollment.STATUS_ENUM.PENDING.value
        }
        context.user_data[Enrollment.ENROLLMENT_DATA].update(event_instance)

        msg = "Choose the role you want to enroll as or click on the Update button to re-enter a event instance code"
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Participant", callback_data=Enrollment.ROLE_ENUM.PARTICIPANT.value),
                InlineKeyboardButton(
                    text="Facilitator", callback_data=Enrollment.ROLE_ENUM.FACILITATOR.value),
            ],
            [
                InlineKeyboardButton(
                    text="Update", callback_data=State.START_OVER.value),
                InlineKeyboardButton(
                    text="Back", callback_data=State.BACK.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        TelegramService.reply_text(msg, update, reply_markup)
        return State.ENROLLMENT_SELECT_ROLE.value

    elif status_code == HTTPStatus.NOT_FOUND:
        msg = "Invalid code, please click *Update* to re-enter or *Back* to return to main menu"
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Update", callback_data=State.START_OVER.value),
                InlineKeyboardButton(
                    text="Back", callback_data=State.BACK.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        TelegramService.reply_text(msg, update, reply_markup)


def enrollment_set_role_callback(update: Update, context: CallbackContext) -> None:
    TelegramService.remove_prev_keyboard(update)
    role = int(TelegramService.get_callback_query_data(update))
    context.user_data[Enrollment.ENROLLMENT_DATA][Enrollment.ROLE] = role

    msg = "Please click submit to confirm enrollment or *Back* to return to main menu"
    keyboard = [
        [
            InlineKeyboardButton(
                text="Submit", callback_data=Enrollment.CHECKOUT)
        ],
        [
            InlineKeyboardButton(
                text="Update", callback_data=State.START_OVER.value),
            InlineKeyboardButton(text="Back", callback_data=State.BACK.value)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    TelegramService.reply_text(msg, update, reply_markup)
    return State.ENROLLMENT_SUBMIT.value


@catch_error
def enrollment_submit_info_callback(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    enrollment_data = context.user_data[Enrollment.ENROLLMENT_DATA]
    serializer = EnrollmentSerializer()
    payload = serializer.dump(enrollment_data)

    user_id = TelegramService.get_user_id(update)
    event_instance_code = enrollment_data.get(EventInstance.CODE)
    enrollment_exist = ApiService.check_enrollment_exist(
        user_id, event_instance_code, context)
    if not enrollment_exist:
        # if float(enrollment_data["fee"]) == 0:
        enrollment, status_code = ApiService.create_enrollment(payload, context)
        if status_code == HTTPStatus.CREATED:
            msg = "Enrolled to course, returning to main menu...."
            context.user_data[State.START_OVER.value] = True
            TelegramService.reply_text(msg, update)
            start.start_callback(update, context)
            return State.BACK.value

        else:
            BackendError(details=status_code)

    else:
        msg = "You are already enrolled, returning to main menu...."
        context.user_data[State.START_OVER.value] = True
        TelegramService.reply_text(msg, update)
        start.start_callback(update, context)
        return State.BACK.value
