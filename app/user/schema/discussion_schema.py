from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DiscussionSchema(BaseModel):
    discussion_id: Optional[int]
    user_id: int
    interlocutor_id: int
    interlocutor_username: str
    interlocutor_profile: Optional[str]
    last_read_date: datetime
    last_message_date: datetime

    @staticmethod
    def from_model(discussion_id: int, user_id: int, interlocutor_id: int, interlocutor_username: str,
                   interlocutor_profile: str, last_read_date: datetime, last_message_date: datetime) -> DiscussionSchema:
        return DiscussionSchema(discussion_id=discussion_id, user_id=user_id,
                                interlocutor_id=interlocutor_id,
                                interlocutor_username=interlocutor_username,
                                interlocutor_profile=interlocutor_profile,
                                last_read_date=last_read_date,
                                last_message_date=last_message_date)
