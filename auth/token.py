from fastapi import Depends, HTTPException, status
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.config import settings
from models.auth import TokenPayLoad
import datetime


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(data: dict, expires_delta: int = None):
    to_encode = {
        "data": data,
    }
    if expires_delta:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
                                            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires_delta})
    
    encoded_jwt = jwt.encode(
                        to_encode, 
                        settings.JWT_SECRET_KEY,
                        algorithm=settings.ALGORITHM)
    
    return encoded_jwt




async def decode_token(token: str = Depends(oauth2_scheme)):
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