from fastapi import APIRouter, WebSocketDisconnect, WebSocket, Depends, status
from models.auth import TokenPayLoad
from connection import ConnectionManager
from auth.token import decode_token_from_ws

from database.intent_database import retrieve_intents
from database.chatbot_model import save_model_state

from typing import Any

from chatbot.train import train_from_db
import functools

router = APIRouter()

manager = ConnectionManager()

@router.websocket("/train")
async def train_model(websocket: WebSocket, token = Depends(decode_token_from_ws)):
    await manager.connect(websocket)
    try:
        if not token:
            raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION, reason="Unauthorized request")
        intents = await retrieve_intents()
        dict_intents = [intent.dict() for intent in intents]
        send = functools.partial(manager.send_response, websocket = websocket)

        train_config: dict[str, Any] = await websocket.receive_json()
        model_state = await train_from_db(dict_intents, send, **train_config)
        # await save_model_state(model_state)
    except WebSocketDisconnect as ws_dc:
        if token:
            manager.disconnect(websocket)
        await manager.send_response({'code': ws_dc.code, 'reason': ws_dc.reason}, websocket)


#TODO
"""
Adjust learning rate dynamicaly

UI

"""
