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
    # State definitions for Event feature
    EVENT_INSTANCE_LIST = 9
    # Meta states
    STOPPING = 10
    SHOWING = 11
    START_OVER = 12 
    # Shortcut to end conversation
    END = ConversationHandler.END


class Constant(Enum):
    
    # Constant definition for authentication
    USERNAME = 13
    EMAIL = 14
    FIRST_NAME = 15
    LAST_NAME = 16
    PASSWORD = 17