from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.token import create_access_token,decode_token
from models.auth import Token, TokenPayLoad, DummyUser
from exception.auth import AuthException, FieldValidationException
from database.auth_database import *

router = APIRouter()

@router.post("/token", response_model = Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
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

@router.post("/register")
async def add_user(user: User):
    print(user)
    invalid_fields_description = {}
    #Don't check if the username is unique if the username isn't valid.
    try:
        clean_username = validate_username(user.username)
    except FieldValidationException as e:
        invalid_fields_description[e.field] = e.description
    else:
        is_user_unique: bool = await check_unique(clean_username)

    if 'username' not in invalid_fields_description and not is_user_unique:
        invalid_fields_description['username'] = 'Username is already taken'

    try:
        clean_password = validate_password(user.password)
    except Exception as e:
        invalid_fields_description[e.field] = e.description

    else:
        user.password = get_password_hash(clean_password)

    if not match_secret(user.secret_pass):
        invalid_fields_description['secret_pass'] = "Secret Pass is incorrect"

    if invalid_fields_description:
        raise AuthException(
            status_code=status.HTTP_409_CONFLICT,
            detail = "Invalid data provided",
            **invalid_fields_description
        )

    new_user = await user.create()
    return {
        'description': 'User successfully created',
        'data': new_user
    }

@router.get("/payload")
async def test(token_payload: TokenPayLoad = Depends(decode_token)):
    return token_payload