from pydantic import BaseModel


class PaymentIntentSchema(BaseModel):
    amount: int
