from pydantic import BaseModel, EmailStr


class AuthenticatedSchema(BaseModel):
    username: str
    token: str
    token_type: str


class Token(BaseModel):
    access_token: str
    token_type: str
