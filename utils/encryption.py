from cryptography.fernet import Fernet
import bcrypt
from dotenv import load_dotenv
from os import getenv
import time

load_dotenv()
TOKEN_SALT = getenv("TOKEN_SALT", "default_salt")  # default fallback

def hash_password(password: str) -> str:
    """
    Hash a password with a secret salt from env.
    Returns the hashed string (utf-8).
    """
    salted_pw = (TOKEN_SALT + password).encode("utf-8")
    hashed = bcrypt.hashpw(salted_pw, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against the hashed value.
    """
    salted_pw = (TOKEN_SALT + password).encode("utf-8")
    return bcrypt.checkpw(salted_pw, hashed.encode("utf-8"))

def generateID(name: str, email: str) -> str:
    ...

def generateToken(name: str, email: str) -> str:
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(TOKEN_SALT.encode() + name.encode() + email.encode() + str(int(time.time())).encode())
    return token.decode()