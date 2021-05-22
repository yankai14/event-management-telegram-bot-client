from dataclasses import dataclass
import requests
from util.config import ENV
from util.constants import Authentication, Other, Enrollment
from telegram.ext import CallbackContext
from http import HTTPStatus
import json

baseURL = "http://127.0.0.1:8000/"

@dataclass
class ApiEndpoints:
    SIGNUP: str = "auth/user"
    LOGIN: str = "auth/login"
    GET_USER: str = "auth/user"
    GET_EVENT_LIST: str = "event"
    GET_EVENT_INSTANCE_LIST: str = "event-instance"
    GET_EVENT_INSTANCE: str = "event-instance"
    GET_ENROLLMENT_LIST: str = "enrollment"
    CREATE_ENROLLMENT: str = "enrollment"

    def __init__(self):
        for attr in dir(self):
            if not attr.startswith("__"):
                setattr(self, attr, baseURL+ getattr(self, attr))


APIEndpoints = ApiEndpoints()

class ApiService:

    @staticmethod
    def get_specific_user(user_id: int):
        response = requests.get(f"{APIEndpoints.GET_USER}/{user_id}")
        user_details = response.json()
        status_code = response.status_code
        return user_details, status_code

    @staticmethod
    def user_already_registered(user_id: int):
        _, status_code = ApiService.get_specific_user(user_id)
        return status_code == HTTPStatus.OK

    @staticmethod
    def signup(registration_data: dict, context: CallbackContext):
        headers = {
            "Content-Type": "application/json"
        }
        registration_data = json.dumps(registration_data)
        response = requests.post(APIEndpoints.SIGNUP, headers=headers, data=registration_data)
        user_details = response.json()
        status_code = response.status_code

        if status_code == HTTPStatus.CREATED:
            del context.user_data[Authentication.REGISTRATION_DATA]
            del context.user_data[Other.CURRENT_FEATURE]

        return user_details, status_code

    @staticmethod
    def login(login_data: dict, context: CallbackContext):
        headers = {
            "Content-Type": "application/json"
        }
        login_data = json.dumps(login_data)
        response = requests.post(APIEndpoints.LOGIN, headers=headers, data=login_data)
        token = response.json().get("token")
        status_code = response.status_code

        if status_code == HTTPStatus.OK:
            context.user_data[Authentication.AUTH_TOKEN] = token
            del context.user_data[Authentication.LOGIN_DATA]
            del context.user_data[Other.CURRENT_FEATURE]

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
    def get_specific_event_instance(event_instance_code: str, context: CallbackContext):
        headers = {
            "Authorization": "Token " + context.user_data.get("AUTH_TOKEN")
        }
        response = requests.get(APIEndpoints.GET_EVENT_INSTANCE_LIST+f'/{event_instance_code}', headers=headers)
        event_instance = response.json()
        status_code = response.status_code
        return event_instance, status_code

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
        if response.json().get("count") > 0:
            enrollment = response.json().get("results")[0] # Will always get 1 enrollment, handled by backend
        else:
            enrollment = None
        status_code = response.status_code
        return enrollment, status_code

    @staticmethod
    def check_enrollment_exist(username: int, event_instance_code: str, context: CallbackContext):
        enrollment, _ = ApiService.get_specific_enrollment(username, event_instance_code, context)

        if enrollment == None:
            return False
            
        return len(enrollment) > 0

    @staticmethod
    def create_enrollment(enrollment_data: dict, context: CallbackContext):
        headers = {
            "Authorization": "Token " + context.user_data.get("AUTH_TOKEN")
        }
        response = requests.post(APIEndpoints.CREATE_ENROLLMENT, data=enrollment_data, headers=headers)
        enrollment = response.json()
        status_code = response.status_code

        if status_code == HTTPStatus.CREATED:
            del context.user_data[Enrollment.ENROLLMENT_DATA]

        return enrollment, status_code


        