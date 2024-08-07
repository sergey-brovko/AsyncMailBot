from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()


FERNET = Fernet(os.getenv('SECRET_KEY'))


def decrypt(encrypted_password) -> str:
    return FERNET.decrypt(encrypted_password).decode()
