from fastapi import APIRouter, Depends
from models.auth import TokenPayLoad
from models.chatbot_state import ModelConfig
from connection import ConnectionManager
from auth.token import decode_token_from_request

from database.intent_database import retrieve_intents
from database.chatbot_model import save_model_state, get_model_config

from chatbot.train import train_from_db


router = APIRouter()

manager = ConnectionManager()


@router.get("/get_config")
async def get_config(token: str = Depends(decode_token_from_request)):
    return await get_model_config()
@router.post('/train_bot')
async def train_bot(model_config: ModelConfig, token: TokenPayLoad = Depends(decode_token_from_request)):
    intents = await retrieve_intents()
    dict_intents = [intent.dict() for intent in intents]
    kwargs = model_config.dict()
    del kwargs['loss']
    chatbot_data_state = await train_from_db(dict_intents, **kwargs)
    kwargs.update({"loss": chatbot_data_state['loss']})
    model_state = await save_model_state(chatbot_data_state, **kwargs)
    return {
        "status": 200,
        "response_type": "success",
        "description": "Bot trained successfully",
        "loss": chatbot_data_state['loss'],
        "data": True
    }