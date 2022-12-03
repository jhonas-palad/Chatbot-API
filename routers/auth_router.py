from fastapi import APIRouter, Depends, Cookie, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.token import create_token, decode_access_token
from models.auth import Token, TokenPayLoad, User
from exception.auth import AuthException, FieldValidationException
from database.auth_database import *
from jose import JWTError ,jwt as _jwt
from config.config import settings

router = APIRouter()

#TODO
#Remove print statements
@router.post("/login", response_model = Token)
async def login_user(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):

    user = await authenticate_user(form_data.username, form_data.password)
    #No user found
    if not user:
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_token(
        {   
            "sub": str(user.id),
            "username": user.username
        },'access')
    #Create refresh token
    refresh_token = create_token(
        {
             "sub": str(user.id),
        }, 'refresh')

    #Save refreshToken with current user
    await user.set({User.refresh_token: refresh_token})
    #Create secure cookie with refresh token
    response.set_cookie(
        'jwt', 
        refresh_token,
        max_age= 24 * 60 * 60 * 1000,
        secure=True,
        httponly=True,
        samesite='none'
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response, jwt: str | None = Cookie(None)):
    """
    Remove the secure cookies and delete the refresh token that is stored
    in the user.
    """
    refresh_token = jwt

    #Don't proceed, return no content
    if not refresh_token:
        return
    
    #Find owner of the token
    found_user = await find_token_owner(refresh_token)

    if found_user:
        #Set to empty string
        await found_user.set({User.refresh_token: ""})

    #Clear the secure cookie
    response.delete_cookie(key="jwt",secure=True, httponly=True, samesite='none')
    
    #Automatically returns None

#TODO
# Add response model
@router.post("/register")
async def add_user(user: User):
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

#TODO
#Remove print statements
@router.get('/refresh', response_model=Token)
async def handle_refresh_token(jwt: str | None = Cookie(None)):
    print(f"JWT: {jwt}")
    if not jwt:
        raise AuthException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to read token from secured cookies",
            headers={"WWW-Authenticate": "Bearer"}
        )
    refresh_token = jwt

    #Find which user holds the token
    found_user = await find_token_owner(refresh_token)

    if not found_user:
        raise AuthException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is not secured",
            headers={"WWW-Authenticate": "Bearer"}
        )

    #Evaluate token
    try:
        payload = _jwt.decode(jwt, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload['sub'] != str(found_user.id):
            raise JWTError("User ID doesn't match")

    except JWTError as e:
        print(e)
        raise AuthException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is not secured",
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        access_token = create_token(
            {
                'sub': payload['sub'],
                'username': found_user.username,
            }, 'access')

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    


