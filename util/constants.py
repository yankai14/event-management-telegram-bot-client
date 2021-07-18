from telegram.ext import ConversationHandler
from enum import Enum


class State(Enum):

    # State definition for top level conversation
    FEATURE_SELECTION = 1
    # State definitions for 2nd level conversation (features)
    EVENT_LIST = 2
    NEW_LAUNCH_INTELLIGENCE = 3
    REGISTER = 4
    LOGIN = 5
    ENROLLMENT_HISTORY = 100
    # State definitions for Enrollment history feature
    ENROLLMENT_HISTORY_SELECTING_ACTION = 101
    ENROLLMENT_HISTORY_GET_INFO = 102
    # State definition for Register feature
    REGISTER_SELECTING_ACTION = 6
    REGISTER_GET_INFO = 7
    REGISTER_SUBMIT = 8
    # State definition for login feature
    LOGIN_SELECTING_ACTION = 9
    LOGIN_GET_INFO = 10
    LOGIN_SUBMIT = 11
    # State definitions for Event feature
    EVENT_INSTANCE_LIST = 12
    # State definitions for Enrollment feature
    ENROLLMENT_SELECTING_ACTION = 13
    ENROLLMENT_GET_INFO = 14
    ENROLLMENT_SUBMIT = 15

    # Meta states
    STOPPING = 16
    SHOWING = 17
    START_OVER = 18 
    # Shortcut to end conversation
    END = ConversationHandler.END


class Other:
    CURRENT_FEATURE = "current_feature"


class Authentication:
    USERNAME = "username"
    PASSWORD = "password"
    EMAIL = "email"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    PASSWORD = "password"
    REGISTRATION_DATA = "registration_data"
    LOGIN_DATA = "login_data"
    AUTH_TOKEN = "AUTH_TOKEN"
    EVENTS = "events"


class Event:
    EVENTS = "events"
    CODE = "eventCode"
    NAME = "name"
    DESCRIPTION = "description"
    LOCATION = "location"


class EventInstance:
    CODE = "eventInstanceCode"
    LOCATION = "location"
    DATES = "dates"
    FEE = "fee"
    IS_COMPLETED = "isCompleted"
    EVENT= "event"
    DATES = "dates"


class EnrollmentRoles(Enum):
    PARTICIPANT_ROLE = 1
    FACILITATOR_ROLE =  2
    ADMIN_ROLE = 3


class EnrollmentStatus(Enum):
    PENDING = 1
    ENROLLED = 2
    REJECTED = 3
    WITHDRAWN = 4


class Enrollment:
    ENROLL = "enroll"
    ENROLLMENT_DATA = "enrollment_data"
    USERNAME = "username"
    ROLE = "role"
    STATUS = "status"
    CHECKOUT = "checkout"
    
    ROLE_ENUM = EnrollmentRoles
    STATUS_ENUM = EnrollmentStatus


class History:
    ENROLLMENT_INFO = "enrollment_info"

    # Data structure
    EVENT_INSTANCE = "eventInstance"
    IS_COMPLETED = "isCompleted"

