from pydantic import BaseModel
from beanie import Document
from typing import Any

class Token(BaseModel):
    access_token: str
    token_type: str
    full_name: str | None = None
    
class TokenPayLoad(BaseModel):
    sub: Any = None
    username: Any = None
    exp: int = None

class User(Document):
    full_name: str | None = None
    secret_pass: str
    refresh_token: str | None = None
    username: str
    password: str
