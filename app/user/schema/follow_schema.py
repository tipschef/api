from datetime import datetime

from pydantic import BaseModel


class FollowSchema(BaseModel):
    username: str
    date: datetime
    is_partner: bool
