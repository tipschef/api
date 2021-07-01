
from pydantic import BaseModel


class CreateSubscriptionSchema(BaseModel):
    subscribed_username: str
    tier: int
    number_month: int
