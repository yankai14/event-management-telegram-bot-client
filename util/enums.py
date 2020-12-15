from telegram.ext import ConversationHandler
from enum import Enum, auto


class State(Enum):

    # State definition for top level conversation
    FEATURE_SELECTION = 1
    # State definitions for 2nd level conversation (features)
    EVENT_LIST = 2
    NEW_LAUNCH_INTELLIGENCE = 3
    REGISTER = 4
    LOGIN = 5
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
    # Meta states
    STOPPING = 13
    SHOWING = 14
    START_OVER = 15 
    # Shortcut to end conversation
    END = ConversationHandler.END


class Constant(Enum):
    
    # Constant definition for authentication
    USERNAME = 16
    EMAIL = 17
    FIRST_NAME = 18
    LAST_NAME = 19
    PASSWORD = 20