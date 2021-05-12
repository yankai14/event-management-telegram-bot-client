from dataclasses import dataclass


@dataclass
class RegistrationData:
    username: int = None
    email: str = None
    first_name: str = None
    last_name: str = None
    password: str = None


@dataclass
class LoginData:
    username: int = None
    password: int = None