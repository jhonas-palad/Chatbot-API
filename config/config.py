from pydantic import BaseSettings
from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.intent import Intent
from models.auth import User
from models.chatbot_state import ModelState


class SettingsNotConfigured(Exception):
    pass
class Settings(BaseSettings):
    #Database env
    DATABASE_URL: Optional[str] = None

    DEV_MODE: int = 0
    #Token env
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM:str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str

    #User
    SECRET_PASS:str
    
    #Chatbot
    CHATBOT_NAME: str = 'asketty'
    LEARNING_RATE_MIN:int | float
    LEARNING_RATE_MAX:int | float
    NUMBER_OF_EPOCHS_MIN:int | float
    NUMBER_OF_EPOCHS_MAX:int | float
    HIDDEN_LAYER_SIZE_MIN:int | float
    HIDDEN_LAYER_SIZE_MAX:int | float

    class Config:
        env_file = './.env'
        orm_mode = True

settings = Settings()


async def initiate_database():
    if not settings.DATABASE_URL:
        raise SettingsNotConfigured(f"Please add DATABASE_URL before starting the app")
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database = client.chatbot_asketty, document_models=[Intent, User, ModelState])


