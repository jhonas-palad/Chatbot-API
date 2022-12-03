from beanie import Document
from datetime import datetime
from typing import Any

class ModelState(Document):
    name: str
    created_time: datetime = datetime.now()
    state: Any = None