from fastapi import WebSocket

from typing import List

class ConnectionManager:
    def __init__(self):
        """
        Create a list of active connections
        """
        self.active_connections: List[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        """
        Accept a WebSocket instance and append it to
        the list of active connections
        """
        for k,v in websocket.__dict__.items():
            print(f"{k}: {v}")
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)
