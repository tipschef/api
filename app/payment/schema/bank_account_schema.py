from pydantic import BaseModel


class BankAccountSchema(BaseModel):
    iban: str
