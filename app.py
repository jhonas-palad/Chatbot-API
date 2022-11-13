from fastapi import FastAPI, Depends
from config.config import initiate_database
from routers.intent_router import router as IntentRouter
from routers.chat_router import router as ChatRouter
description = """
    This implements a websocket API for mobile application 🤖.
"""


app = FastAPI(
    title = "Asketty Chatbot application",
    version="0.0.1",
    description=description,
    contact={
        "name": "Jhonas Emmanuel O. Palad",
        "email": "jhonasemmanuel@gmail.com"
    }

)


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get('/', tags=["Root"])
async def root_endpoint():
    return {'message': 'Welcome to asketty app'}

app.include_router(IntentRouter, tags=["Intent"], prefix="/intent")
app.include_router(ChatRouter, tags=["Chat"], prefix="/chat")