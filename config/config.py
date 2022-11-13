from pydantic import BaseSettings
from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.intent import Intent

class SettingsNotConfigured(Exception):
    pass
class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    MONGO_INITDB_DATABASE: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_ROOT_USERNAME: str

    class Config:
        env_file = './.env'
        orm_mode = True

settings = Settings()

async def initiate_database():

    if not settings.DATABASE_URL:
        raise SettingsNotConfigured(f"Please add DATABASE_URL before starting the app")
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database = client.chatbot_asketty, document_models=[Intent])


