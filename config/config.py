from pydantic import BaseSettings
from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.intent import Intent, IntentDev
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
    class Config:
        env_file = './.env'
        orm_mode = True

settings = Settings()


async def initiate_database():
    IntentModel = Intent if not settings.DEV_MODE else IntentDev
    if not settings.DATABASE_URL:
        raise SettingsNotConfigured(f"Please add DATABASE_URL before starting the app")
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database = client.chatbot_asketty, document_models=[IntentModel, User, ModelState])


