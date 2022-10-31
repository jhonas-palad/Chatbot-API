from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect

from connection import ConnectionManager

import uvicorn
import os

from dotenv import load_dotenv

load_dotenv()

chat = APIRouter()

manager = ConnectionManager()

@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket = WebSocket):
    """
    Will open a WebSocket to send messages between client and server.
    Infinite loop to ensure that the socket stays open. Except when there
    socket gets disconnected. While the connection is open we receive any
    messages sent by the client with websocket.recieve_text and send back
    a response
    """
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = {'response': 'TEST SERVER'}
            await manager.send_message({"data": data}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


api = FastAPI()
api.include_router(chat)

if __name__ == '__main__':
    
    if os.environ.get('APP_ENV') == 'development':
        uvicorn.run("main:api", reload=True)
    else:
        uvicorn.run("main:api")