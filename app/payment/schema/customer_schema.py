from pydantic import BaseModel


class CustomerSchema(BaseModel):
    email: str
    name: str
    phone: str
