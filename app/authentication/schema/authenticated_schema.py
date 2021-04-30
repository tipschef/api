from pydantic import BaseModel, EmailStr


class AuthenticatedSchema(BaseModel):
    email: EmailStr
    token: str
