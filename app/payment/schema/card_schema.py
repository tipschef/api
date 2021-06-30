from pydantic import BaseModel


class CardSchema(BaseModel):
    number: str
    exp_month: int
    exp_year: int
    cvc: str
