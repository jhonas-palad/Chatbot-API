from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import initiate_database
from routers.intent_router import router as IntentRouter
from routers.chat_router import router as ChatRouter
from routers.auth_router import router as AuthRouter


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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get('/', tags=["Root"])
async def root_endpoint():

    return {'message': f'Welcome to asketty app'}


app.include_router(IntentRouter, tags=["Intent"], prefix="/intent")
app.include_router(ChatRouter, tags=["Chat"], prefix="/chat")
app.include_router(AuthRouter, tags=["Authentication"], prefix="/auth")