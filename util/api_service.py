from dataclasses import dataclass

baseURL = "http://127.0.0.1:8000/"

@dataclass
class ApiEndpoints:
    SIGNUP: str = "auth/user"
    LOGIN: str = "auth/login"
    GET_EVENT_LIST: str = "event"
    GET_EVENT_INSTANCE_LIST: str = "event-instance"
    GET_EVENT_INSTANCE: str = "event-instance"
    GET_ENROLLMENT_LIST: str = "enrollment"
    CREATE_ENROLLMENT: str = "enrollment"

    def __post__init__(self):
        for attr in dir(self):
            if not attr.startswith("__"):
                setattr(self, attr, baseURL+ getattr(self, attr))


APIEndpoints = ApiEndpoints()