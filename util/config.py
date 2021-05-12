from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

@dataclass
class ENVIRONMENT_VARIABLES:
    TELEGRAM_BOT_TOKEN:str = os.getenv("TELEGRAM_BOT_TOKEN")
    PAYMENT_TOKEN:str = os.getenv("PAYMENT_TOKEN")
    MAIL_PORT:str = os.getenv("MAIL_PORT")
    MAIL_ADDRESS:str = os.getenv("MAIL_ADDRESS")
    MAIL_PASSWORD:str = os.getenv("MAIL_PASSWORD")


ENV = ENVIRONMENT_VARIABLES()
