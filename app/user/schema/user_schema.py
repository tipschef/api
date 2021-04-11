from app.user.schema.user_base_schema import UserBase


class User(UserBase):
    id: int

    class Config:
        orm_mode = True