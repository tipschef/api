from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.user.schema.received_message_schema import ReceivedMessageSchema


class SendMessageSchema(BaseModel):
    receiver_id: int
    sender_id: int
    content: str
    date_create: datetime

    @staticmethod
    def from_received_message(received_message: ReceivedMessageSchema, date_create: datetime):
        return SendMessageSchema(receiver_id=received_message.receiver_id,
                                 sender_id=received_message.sender_id,
                                 content=received_message.content,
                                 date_create=date_create)

    @staticmethod
    def from_data(receiver_id: int, sender_id: int, content: str, date_create: datetime):
        return SendMessageSchema(receiver_id=receiver_id,
                                 sender_id=sender_id,
                                 content=content,
                                 date_create=date_create)
