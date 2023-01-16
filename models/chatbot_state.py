from beanie import Document
from datetime import datetime
from pydantic import BaseModel
from typing import Any

class ModelConfig(BaseModel):
    num_epochs: int
    learning_rate: float
    hidden_layer_size: int
    loss: float

class ModelState(Document):
    name: str
    created_time: datetime = datetime.now()
    state: Any = None
    config: ModelConfig