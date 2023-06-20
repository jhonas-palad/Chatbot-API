from fastapi import APIRouter, Depends, status
from auth.token import decode_token_from_request
from models.auth import TokenPayLoad
from database.intent_database import *
from models.intent import *
from chatbot.train import train_from_db
from exception.intent import IntentException
from database.chatbot_model import *
import asyncio
router = APIRouter()

@router.get('/all', response_description="Intents retrieved", response_model=IntentResponse)
async def get_all_intents(token: TokenPayLoad = Depends(decode_token_from_request)):
    intents = await retrieve_intents()
    return {
        "status": 200,
        "response_type": "success",
        "description": "Intents data retrieve successfully",
        "data": intents
    }

@router.get('/get/{id}', response_description="Intent data retrieved", response_model=IntentResponse)
async def get_intent_data(id: str, token: TokenPayLoad = Depends(decode_token_from_request)):
    try:
        id = PydanticObjectId(id)
    except Exception:
        intent = None
    else:
        intent = await retrieve_intent(id)
    if not intent:
        raise IntentException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intent doesn't exist"
        )

    return {
        "status": 200,
        "response_type": "success",
        "description": "Intent retrieved successfully",
        "data": intent
    }


@router.post("/create", response_description="Intent data added into the database", response_model = IntentResponse)
async def add_intent_data(intent:Intent, token: TokenPayLoad = Depends(decode_token_from_request)):
    new_intent = await add_intent(intent)
    if not new_intent:
        raise IntentException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Intent tag is already registered. Tag must be unique"
        ) 
    return {
        "status": 200,
        "response_type": "success",
        "description": "Intents data saved successfully",
        "data": new_intent
    }


@router.put("/update/{id}", response_model=IntentResponse)
async def update_intent_data(id: str, req: UpdateIntent, token: TokenPayLoad = Depends(decode_token_from_request)):
    try:
        id = PydanticObjectId(id)
    except Exception:
        updated_intent = None
    else:
        updated_intent = await update_intent(id, req.dict())
    if not updated_intent:
        raise IntentException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Intent doesn't exist" if update_intent is None else "Tag is already registered"
        )
    return {
        "status": 200,
        "response_type": "success",
        "description": f"Intent with ID:{id} updated successfully",
        "data": updated_intent
    }

@router.delete('/delete/{id}', response_description="Intent data removed from the database")
async def delete_intent_data(id: str, token: TokenPayLoad = Depends(decode_token_from_request)):
    try:
        id = PydanticObjectId(id)
    except Exception:
        deleted_intent = False
    else:
        deleted_intent = await delete_intent(id)
    if not deleted_intent:
        raise IntentException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intent doesn't exist"
        )
    return {
        "status": 200,
        "response_type": "success",
        "description": f"Intent with ID:{id} deleted successfully",
        "data": deleted_intent
    }

@router.post('/train_bot', response_description="Train the chatbot model")
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
