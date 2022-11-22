from pydantic import BaseModel
from beanie import Document
from typing import Any

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayLoad(BaseModel):
    data: Any = None
    exp: int = None

class User(Document):
    full_name: str | None = None
    secret_pass: str
    username: str
    password: str
