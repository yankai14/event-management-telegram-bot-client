from test import START_OVER
from telegram.ext import ConversationHandler


class State:

    # State definition for top level conversations
    FEATURE_SELECTION = map(chr, range(1))

    # State definitions for 2nd level conversations
    EVENT_LIST, NEW_LAUNCH_INTELLIGENCE = map(chr, range(1,3))

    # State definitions for Event feature
    EVENT_INSTANCE_LIST = map(chr, range(4))

    # Meta states
    STOPPING, SHOWING, START_OVER = map(chr, range(5,8))

    # Shortcut to end conversation
    END = ConversationHandler.END
