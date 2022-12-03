from fastapi import APIRouter, WebSocketDisconnect, WebSocket
from database.chatbot_model import fetch_model_states
from database.intent_database import retrieve_intents
from connection import ConnectionManager

from chatbot import init_bot

router = APIRouter()

manager = ConnectionManager()

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket = WebSocket):
    """
    Will open a WebSocket to send messages between client and server.
    Infinite loop to ensure that the socket stays open. Except when there
    socket gets disconnected. While the connection is open we receive any
    messages sent by the client with websocket.recieve_text and send back
    a response
    """
    all_intents = await retrieve_intents()
    model_state = await fetch_model_states()
    cb = init_bot(model_state, all_intents)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = cb.get_response(data)
            await manager.send_response(data, websocket)
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)