from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import initiate_database
from routers.intent_router import router as IntentRouter
from routers.chat_router import router as ChatRouter
from routers.auth_router import router as AuthRouter
from exception.intent import IntentException, intent_exception_handler
from exception.auth import *

description = """
    This implements a websocket API for mobile application 🤖.
"""
app = FastAPI(
    title = "Asketty Chatbot application",
    version="0.0.2",
    description=description,
    contact={
        "name": "Jhonas Emmanuel O. Palad",
        "email": "jhonasemmanuel@gmail.com"
    }

)

origins = [
    "http://localhost:3000",
    "http://139.162.82.172"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.add_exception_handler(AuthException, auth_exception_handler)
app.add_exception_handler(IntentException, intent_exception_handler)

app.include_router(IntentRouter, tags=["Intent"], prefix="/intent")
app.include_router(ChatRouter, tags=["Chat"], prefix="/chat")
app.include_router(AuthRouter, tags=["Authentication"], prefix="/auth")

@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get('/api/root', tags=["Root"])
async def root_endpoint():
    return {'message': 'Welcome to asketty app'}