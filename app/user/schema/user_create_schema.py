from app.user.schema.user_base_schema import UserBase


class UserCreate(UserBase):
    password: str
