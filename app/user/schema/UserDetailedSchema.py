from pydantic import EmailStr

from app.user.model.user_model import UserModel
from app.user.schema.user_base_schema import UserBaseSchema


class UserDetailedSchema(UserBaseSchema):
    likes: int
    followers: int

    @staticmethod
    def from_user_model(user: UserModel, likes: int, followers: int):
        return UserDetailedSchema(email=EmailStr(user.email),
                                  username=user.username,
                                  likes=likes,
                                  followers=followers)
