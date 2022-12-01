from passlib.context import CryptContext
from models.auth import User
from config.config import settings
from exception.auth import FieldValidationException
import re
user_collection = User

USERNAME_REGEX = r"^[a-zA-Z][a-zA-Z0-9-_]{3,23}$"
PWD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$]).{8,24}$"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Compares the given password against the hashed password,
    returns True if they are equal.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Generates a password hash using the CyptContext instance with
    specified scheme.
    """
    return pwd_context.hash(password)

def validate_username(username: str) -> str:
    matched_username = re.match(USERNAME_REGEX, username)
    if matched_username is None:
        raise FieldValidationException(
            field = 'username',
            description='Username is invalid'
        )
    return matched_username.string

def validate_password(password: str) -> str:
    matched_password = re.match(PWD_REGEX, password)
    if matched_password is None:
        raise FieldValidationException(
            field = 'password',
            description='Password is invalid'
        )
    return matched_password.string

def match_secret(secret: str) -> bool:
    return settings.SECRET_PASS == secret

async def get_user_by_username(username: str) -> User:
    user = await user_collection.find_one(User.username == username)
    return user

async def find_token_owner(jwt: str) -> User:
    user = await user_collection.find_one(User.refresh_token == jwt)
    return user

async def authenticate_user(username: str, password: str) -> User | bool:
    user = await get_user_by_username(username)
    if not user:
        """
        no user found
        """
        return False
    if not verify_password(password, user.password):
        """
        password incorrect
        """
        return False

    return user


async def check_unique(username: str) -> bool:
    user = await get_user_by_username(username)
    return not user
