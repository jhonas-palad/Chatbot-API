from fastapi import APIRouter, WebSocketDisconnect, WebSocket, Depends, status, Cookie
from models.auth import TokenPayLoad
from connection import ConnectionManager
from auth.token import decode_token_from_ws, decode_token_from_request

from database.intent_database import retrieve_intents
from database.chatbot_model import save_model_state, get_model_config

from typing import Any

from chatbot.train import train_from_db
import functools

router = APIRouter()

manager = ConnectionManager()


@router.get("/get_config")
async def get_config(token: str = Depends(decode_token_from_request)):
    return await get_model_config()

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
        train_config['loss'] = model_state.get('loss')
        saved_model_state = await save_model_state(model_state, **train_config)
        await send(saved_model_state.config.dict())
    except WebSocketDisconnect as ws_dc:
        manager.disconnect(websocket)
        if not token:
            await websocket.close(code=ws_dc.code, reason=ws_dc.reason)