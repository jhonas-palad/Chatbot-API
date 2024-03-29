from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer

from starlette.datastructures import Headers

from jose import jwt
from config.config import settings
from models.auth import TokenPayLoad
from typing import Literal, Mapping
import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_token(data: dict, _type:Literal['access', 'refresh']='access'):
    to_encode = {
        **data
    }
    minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES if _type == 'access' \
              else settings.REFRESH_TOKEN_EXPIRE_MINUTES
    expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
                                        minutes=minutes)
    to_encode.update({"exp": expires_delta})
    sign_key = settings.JWT_SECRET_KEY if _type == 'access' else settings.JWT_REFRESH_SECRET_KEY
    encoded_jwt = jwt.encode(
                        to_encode, 
                        sign_key,
                        algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_token(token:str, from_ws: bool = False) -> TokenPayLoad:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY if not from_ws else settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayLoad(**payload)
    except Exception as e:
        if from_ws:
            return None
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

def decode_token_from_request(token:str = Depends(oauth2_scheme)) -> TokenPayLoad:
    return decode_token(token)

def decode_token_from_ws(jwt: str | None = Cookie(None)) -> TokenPayLoad:
    return decode_token(jwt, from_ws=True)
    



