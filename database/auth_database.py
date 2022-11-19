from passlib.context import CryptContext
from models.auth import User

user_collection = User

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

async def get_user(email: str) -> User:
    user = await user_collection.find_one(User.email == email)
    return user


async def authenticate_user(email: str, password: str) -> User | bool:
    user = await get_user(email)
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

