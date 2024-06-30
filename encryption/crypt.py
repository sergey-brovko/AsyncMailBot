from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()


FERNET = Fernet(os.getenv('SECRET_KEY'))


def encrypt(password):
    return FERNET.encrypt(password.encode()).decode()


def decrypt(encrypted_password):
    return FERNET.decrypt(encrypted_password).decode()
