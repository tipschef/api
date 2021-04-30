from pydantic import BaseModel, EmailStr, SecretStr, validator


class AuthenticationSchema(BaseModel):
    email: EmailStr
    password: SecretStr

    @classmethod
    @validator('password')
    def password_should_be_encoded(cls, value: str) -> SecretStr:
        return SecretStr(value)



