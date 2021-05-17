from pydantic import BaseModel, SecretStr, validator


class AuthenticationSchema(BaseModel):
    username: str
    password: SecretStr

    @classmethod
    @validator('password')
    def password_should_be_encoded(cls, value: str) -> SecretStr:
        _ = cls
        return SecretStr(value)
