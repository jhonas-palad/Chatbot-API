from models.chatbot_state import ModelState
from datetime import datetime
import pickle

async def save_model_state(model_state: dict):
    pickled_model_state = pickle.dumps(model_state)

    model_state = await ModelState.find_one(ModelState.name == 'asketty')
    if not model_state:
        return await ModelState(
            name = 'asketty',
            state = pickled_model_state
        ).create()
    update_query = {
        "$set": {
            'state': pickled_model_state,
            'created_time': datetime.now()
        }
    }
    updated_model_state = await model_state.update(update_query)
    return updated_model_state

async def fetch_model_states():
    model = await ModelState.find_one(ModelState.name == 'asketty')
    try:
        model_state = pickle.loads(model.state)
    except Exception as e:
        print(f"Pickleee {e}")
    return model_state
