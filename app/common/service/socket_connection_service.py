from typing import List

from fastapi import WebSocket

from app.user.schema.send_message_schema import SendMessageSchema


class SocketConnectionService:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_to_received(self, message: SendMessageSchema):
        for connection in self.active_connections:
            if connection.url.__str__().split('/')[-2] == str(message.receiver_id):
                await connection.send_text(message.json())


manager = SocketConnectionService()
