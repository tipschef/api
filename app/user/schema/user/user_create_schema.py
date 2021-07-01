from pydantic import SecretStr, validator

from app.user.schema.user.user_base_schema import UserBaseSchema


class UserCreateSchema(UserBaseSchema):
    password: SecretStr

    @classmethod
    @validator('password')
    def encode_password(cls, value: str):
        _ = cls
        return SecretStr(value)
