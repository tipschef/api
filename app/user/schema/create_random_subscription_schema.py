
from pydantic import BaseModel


class CreateRandomSubscriptionSchema(BaseModel):
    subscribed_username: str
    tier: int
    number: int
