from __future__ import annotations

from pydantic import BaseModel


class ReceivedMessageSchema(BaseModel):
    receiver_id: int
    sender_id: int
    content: str

    @staticmethod
    def from_json(json: dict):
        return ReceivedMessageSchema(receiver_id=json['receiver_id'], sender_id=json['sender_id'], content=json['content'])
