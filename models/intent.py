from typing import Optional, List, Any

from beanie import Document
from pydantic import BaseModel


class Intent(Document):
    tag: str
    patterns: List[str]
    responses: List[str]
    follow_up_responses: List[str]

class UpdateIntentModel(BaseModel):
    tag: Optional[str]
    patterns: Optional[List[str]]
    responses: Optional[List[str]]
    follow_up_responses: Optional[List[str]]

class IntentResponse(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

