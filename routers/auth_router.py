from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.token import create_access_token,decode_token
from models.auth import Token, TokenPayLoad
from database.auth_database import *


router = APIRouter()

@router.post("/token", response_model = Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user.dict())
    access_token = create_access_token(
        {
            "_id": str(user.id),
            "full_name": user.full_name
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.post("/add_user")
async def add_user(user: User):
    user.password = get_password_hash(user.password)
    user = await user.create()
    return {
        'status_code': 200,
        'data': user
    }

@router.get("/sample")
async def test(token: TokenPayLoad = Depends(decode_token)):
    return token