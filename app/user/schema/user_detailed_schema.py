from typing import Optional

from pydantic import EmailStr

from app.recipe.model.media.media_model import MediaModel
from app.user.model.user_model import UserModel
from app.user.schema.user_base_schema import UserBaseSchema


class UserDetailedSchema(UserBaseSchema):
    likes: int
    followers: int
    description: Optional[str]
    profile_url: str
    background_url: str

    @staticmethod
    def from_user_model(user: UserModel, likes: int, followers: int, description: str, profile: MediaModel,
                        background: MediaModel):
        return UserDetailedSchema(email=EmailStr(user.email),
                                  username=user.username,
                                  likes=likes,
                                  followers=followers, description=description,
                                  profile_url=profile.path if profile is not None else "",
                                  background_url=background.path if background is not None else "")
