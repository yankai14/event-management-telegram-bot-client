from dataclasses import dataclass, asdict
import requests
from util.config import ENV
from telegram import Update
from telegram.ext import CallbackContext
from http import HTTPStatus

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

class ApiService:

    @staticmethod
    def get_specific_user(user_id: int):
        response = requests.get(f"http://127.0.0.1:8000/auth/user/{user_id}")
        user_details = response.json()
        status_code = response.status_code
        return user_details, status_code

    @staticmethod
    def user_already_registered(user_id: int):
        user_details, status_code = ApiService.get_specific_user(user_id)
        return status_code == HTTPStatus.OK

    @staticmethod
    def signup(registration_data: dict, context: CallbackContext):
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(APIEndpoints.SIGNUP, headers=headers, data=registration_data)
        user_details = response.json()
        status_code = response.status_code

        if status_code == HTTPStatus.CREATED:
            context.user_data["AUTH_TOKEN"] = response.json().get("token")
            del context.user_data["registration_data"]
            del context.user_data["current_feature"]

        return user_details, status_code

    @staticmethod
    def login(login_data: dict, context: CallbackContext):
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(APIEndpoints.SIGNUP, headers=headers, data=login_data)
        token = response.json().get("token")
        status_code = response.status_code

        if status_code == HTTPStatus.CREATED:
            context.user_data["AUTH_TOKEN"] = token
            del context.user_data["login_data"]
            del context.user_data["current_feature"]

        return token, status_code

    @staticmethod
    def get_event_list(context: CallbackContext):
        headers = {
            "Authorization": "Token " + context.user_data.get("AUTH_TOKEN")
        }
        response = requests.get(APIEndpoints.GET_EVENT_LIST, headers=headers)
        events = response.json().get("results")
        status_code = response.status_code
        return events, status_code

    @staticmethod
    def get_event_instance_list(event_code: str, context: CallbackContext):
        headers = {
            "Authorization": "Token " + context.user_data.get("AUTH_TOKEN")
        }
        params = {
            "isCompleted": "False",
            "eventCode": event_code
        }
        response = requests.get(APIEndpoints.GET_EVENT_INSTANCE_LIST, headers=headers, params=params)
        event_instances = response.json().get("results")
        status_code = response.status_code
        return event_instances, status_code

    @staticmethod
    def get_specific_enrollment(username, event_instance_code, context: CallbackContext):
        headers = {
            "Authorization": "Token " + context.user_data.get("AUTH_TOKEN")
        }
        params = {
            "user": username,
            "eventInstance": event_instance_code
        }
        response = requests.get(APIEndpoints.GET_ENROLLMENT_LIST, headers=headers, params=params)
        enrollment = response.json().get("results")[0] # Will always get 1 enrollment, handled by backend
        status_code = response.status_code
        return enrollment, status_code

    @staticmethod
    def check_enrollment_exist(username: int, event_instance_code: str, context: CallbackContext):
        enrollment = ApiService.get_specific_enrollment(username, event_instance_code, context)
        return enrollment.get("count") != 0

    @staticmethod
    def create_enrollment(enrollment_data: dict, context: CallbackContext):
        headers = {
            "Authorization": "Token " + context.user_data.get("AUTH_TOKEN")
        }
        response = requests.post("http://127.0.0.1:8000/enrollment", data=enrollment_data, headers=headers)
        enrollment = response.json()
        status_code = response.status_code
        return enrollment, status_code


        
