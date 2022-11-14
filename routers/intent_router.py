from fastapi import APIRouter

from database.database import *
from models.intent import *
from chatbot.train import train_from_db
router = APIRouter()


@router.get('/', response_description="Intents retrieved", response_model=IntentResponse)
async def get_all_intents():
    intent = await retrieve_intents()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Intents data retrieve successfully",
        "data": intent
    }

@router.get('/{id}', response_description="Intent data retrieved", response_model=IntentResponse)
async def get_intent_data(id: str):
    try:
        id = PydanticObjectId(id)
    except Exception:
        intent = None
    else:
        intent = await retrieve_intent(id)
    return {
        "status_code": 200 if intent else 404,
        "response_type": "success" if intent else "error",
        "description": "Intent retrieved successfully" if intent else "Intent doesn't exist",
        "data": intent
    }


@router.post("/", response_description="Intent data added into the database", response_model = IntentResponse)
async def add_intent_data(intent: Intent):
    new_intent = await add_intent(intent)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Intents data saved successfully",
        "data": new_intent
    }


@router.put("/update/{id}", response_model=IntentResponse)
async def update_intent_data(id: str, req: UpdateIntentModel):
    try:
        id = PydanticObjectId(id)
    except Exception:
        updated_intent = None
    else:
        updated_intent = await update_intent(id, req.dict())
    return {
        "status_code": 200 if updated_intent else 404,
        "response_type": "success" if updated_intent else "error",
        "description": f"Intent with ID:{id} updated successfully" if updated_intent else f"An error occurred. Intent with ID:{id} not found.",
        "data": updated_intent
    }

@router.delete('/{id}', response_description="Intent data removed from the database")
async def delete_intent_data(id: str):
    try:
        id = PydanticObjectId(id)
    except Exception:
        deleted_intent = False
    else:
        deleted_intent = await delete_intent(id)

    return {
        "status_code": 200 if deleted_intent else 404,
        "response_type": "success" if deleted_intent else "error",
        "description": f"Intent with ID:{id} deleted successfully" if deleted_intent else f"An error occurred. Intent with ID:{id} not found.",
        "data": deleted_intent
    }

@router.post('/train_bot', response_description="Train the chatbot model")
async def train_bot():
    intents = await retrieve_intents()
    dict_intents = [intent.dict() for intent in intents]
    train_from_db(dict_intents)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Bot trained successfully",
        "data": intents
    }
