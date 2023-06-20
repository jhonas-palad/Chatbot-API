from models.chatbot_state import ModelState, ModelConfig
from datetime import datetime
import pickle
from config import settings
import re

MODEL_NAME = settings.CHATBOT_NAME

async def save_model_state(model_state: dict, **config):
    pickled_model_state = pickle.dumps(model_state)

    model_state = await ModelState.find_one(ModelState.name == MODEL_NAME)
    model_config = ModelConfig(**config)
    if not model_state:
        ms = ModelState(
            name = MODEL_NAME,
            state = pickled_model_state,
            config = model_config
        )
        return await ms.create()
    update_query = {
        "$set": {
            'state': pickled_model_state,
            'created_time': datetime.now(),
            'config': model_config.dict()
        }
    }
    await model_state.update(update_query)
    return model_state

async def fetch_model_states():
    model = await ModelState.find_one(ModelState.name == MODEL_NAME)
    try:
        model_state = pickle.loads(model.state)
    except Exception as e:
        print(f"Pickleee Error {e}")
    return model_state

async def get_model_config() -> ModelConfig:
    model = await ModelState.find_one(ModelState.name == MODEL_NAME)
    max_min_re = r"^.*_(MAX|MIN)$"
    config = {
        k.lower(): v for k, v in settings.dict().items() if \
        re.match(max_min_re, k, re.IGNORECASE)
    }
    config.update(model.config.dict())
    return config