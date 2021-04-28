from pydantic import SecretStr

from app.user.schema.user_base_schema import UserBaseSchema


class UserCreateSchema(UserBaseSchema):
    password: SecretStr
