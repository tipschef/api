from pydantic import BaseModel


class AuthenticatedSchema(BaseModel):
    username: str
    token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    token_type: str
