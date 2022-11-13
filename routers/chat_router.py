from fastapi import APIRouter, WebSocketDisconnect, WebSocket

from connection import ConnectionManager

from chatbot import cb

router = APIRouter()

manager = ConnectionManager()

@router.websocket("/")
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
            data = cb.get_response(data)
            await manager.send_response(data, websocket)
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)