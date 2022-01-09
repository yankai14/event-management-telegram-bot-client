from telegram.ext import ConversationHandler
from enum import Enum


class State(Enum):

    # State definition for top level conversation
    FEATURE_SELECTION = 1
    # State definitions for 2nd level conversation (features)
    EVENT_LIST = 100
    NEW_LAUNCH_INTELLIGENCE = 101
    REGISTER = 102
    LOGIN = 103
    ENROLLMENT_HISTORY = 104
    ENROLLMENT_PAYMENT = 105

    # State definitions for Enrollment history feature
    ENROLLMENT_HISTORY_SELECTING_ACTION = 200
    ENROLLMENT_HISTORY_GET_INFO = 201
    # State definition for Register feature
    REGISTER_SELECTING_ACTION = 300
    REGISTER_GET_INFO = 301
    REGISTER_SUBMIT = 302
    # State definition for login feature
    LOGIN_SELECTING_ACTION = 400
    LOGIN_GET_INFO = 401
    LOGIN_SUBMIT = 402
    # State definitions for Event feature
    EVENT_SELECTING_ACTION = 500
    EVENT_INSTANCE_LIST = 501
    # State definitions for Enrollment feature
    ENROLLMENT_SELECTING_ACTION = 601
    ENROLLMENT_GET_INFO = 602
    ENROLLMENT_SELECT_ROLE = 603
    ENROLLMENT_SUBMIT = 604
    ENROLLMENT_PAYMENT_GET_INFO = 701

    #State definitions for Pagination
    EVENT_PAGINATION = 801
    EVENT_INSTANCE_PAGINATION = 802
    ENROLLMENT_HISTORY_PAGINATION = 803


    # Meta states
    STOPPING = 1000
    SHOWING = 1001
    START_OVER = 1002 
    BACK = 1003
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
    IS_OPEN_FOR_SIGNUPS = "isOpenForSignUps"
    EVENT= "event"
    DATES = "dates"


class EnrollmentRoles(Enum):
    PARTICIPANT = 1
    FACILITATOR = 2
    EVENT_ADMIN = 3
    COORDINATOR = 4
    LEAD = 5


class EnrollmentStatus(Enum):
    PENDING = 1
    ENROLLED = 2
    REJECTED = 3
    WITHDRAWN = 4
    AWATING_PAYMENT = 5


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


class Payment:
    ENROLLMENT_PAYMENT_INFO = "enrollment_payment_info"
    PAYMENT_ID = "paymentId"

class Folder:
    # Data structure
    EVENT_INSTANCE = "eventInstance"
    FOLDER_ID = "folderId"
    FOLDER_NAME = "folderName"


class FolderPermissionRoles(Enum):
    READER = "reader"
    WRITER = "writer"
    ORGANIZER = "organizer"


class FolderPermission:
    # Data structure
    FOLDER = "folder"
    USER = "user"
    PERMISSION_ID = "permissionId"
    FOLDER_ROLE = "folderRole"

    FOLDER_ROLE_ENUM = FolderPermissionRoles