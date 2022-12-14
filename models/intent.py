from typing import Optional, List, Any

from beanie import Document
from pydantic import BaseModel

class Entity(BaseModel):
    title: str
    text: str

class Intent(Document):
    tag: str
    patterns: List[str]
    responses: List[str]
    entities: List[Entity]
class UpdateIntent(BaseModel):
    tag: Optional[str]
    patterns: Optional[List[str]]
    responses: Optional[List[str]]
    entities: Optional[List[Entity]]

class IntentResponse(BaseModel):
    status: int
    response_type: str
    description: str
    data: Optional[Any]
