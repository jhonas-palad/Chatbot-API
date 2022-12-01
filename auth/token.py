from fastapi import Depends, HTTPException, status
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.config import settings
from models.auth import TokenPayLoad
from typing import Literal
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
    print(f"{_type}{sign_key}")
    encoded_jwt = jwt.encode(
                        to_encode, 
                        sign_key,
                        algorithm=settings.ALGORITHM)
    
    return encoded_jwt


async def decode_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayLoad(**payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

#TODO
#Refresh token exp
#Logout
#Refresh Token sign key