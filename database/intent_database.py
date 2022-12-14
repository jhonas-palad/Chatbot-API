from typing import List, Union
from beanie import PydanticObjectId
from models.intent import Intent, IntentDev

intent_collection = Intent

async def add_intent(new_intent: Intent | IntentDev) -> Intent:
    intent = await new_intent.create()
    return intent

async def retrieve_intents() -> List[Intent | IntentDev]:
    intent = await intent_collection.all().to_list()
    return intent

async def retrieve_intent(id: PydanticObjectId) -> Intent:
    intent = await intent_collection.get(id)
    if intent:
        return intent

async def delete_intent(id: PydanticObjectId) -> bool:
    intent = await intent_collection.get(id)
    if intent:
        await intent.delete()
        return True
    return False

async def update_intent(id: PydanticObjectId, data: dict) -> Union[bool, Intent]:
    body = {k: v for k, v in data.items() if v is not None}

    update_query = {
        "$set": {
            field: value for field, value in body.items()
        }
    }
    intent = await intent_collection.get(id)
    if intent:
        await intent.update(update_query)
        return intent
    return False


