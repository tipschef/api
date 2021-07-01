from typing import Optional

from pydantic import EmailStr

from app.recipe.model.media.media_model import MediaModel
from app.user.model.user_model import UserModel
from app.user.schema.user.user_base_schema import UserBaseSchema


class UserDetailedSchema(UserBaseSchema):
    likes: int
    followers: int
    subscribers: Optional[int]
    recipes: Optional[int]
    description: Optional[str]
    profile_url: str
    background_url: str
    following: Optional[bool]
    firstname: Optional[str]
    lastname: Optional[str]
    is_partner: bool

    @staticmethod
    def from_user_model(user: UserModel, likes: int, followers: int, description: str, profile: MediaModel,
                        background: MediaModel):
        return UserDetailedSchema(email=EmailStr(user.email),
                                  username=user.username,
                                  likes=likes,
                                  followers=followers, description=description,
                                  profile_url=profile.path if profile is not None else "",
                                  background_url=background.path if background is not None else "",
                                  is_partner=user.is_partner)

    @staticmethod
    def from_user_model_with_follow(user: UserModel, likes: int, followers: int, description: str, profile: MediaModel,
                                    background: MediaModel, following: bool):
        return UserDetailedSchema(email=EmailStr(user.email),
                                  username=user.username,
                                  likes=likes,
                                  following=following,
                                  followers=followers, description=description,
                                  profile_url=profile.path if profile is not None else "",
                                  background_url=background.path if background is not None else "",
                                  is_partner=user.is_partner)

    @staticmethod
    def from_user_model_with_data(user: UserModel, likes: int, followers: int, description: str, profile: MediaModel,
                                  background: MediaModel, following: bool, subscribers: int, recipes: int):
        return UserDetailedSchema(email=EmailStr(user.email),
                                  username=user.username,
                                  likes=likes,
                                  following=following,
                                  subscribers=subscribers,
                                  recipes=recipes,
                                  followers=followers, description=description,
                                  profile_url=profile.path if profile is not None else "",
                                  background_url=background.path if background is not None else "",
                                  is_partner=user.is_partner)

    @staticmethod
    def from_user_model_with_name(user: UserModel, likes: int, followers: int, description: str, profile: MediaModel,
                                  background: MediaModel, following: bool, firstname: str, lastname: str):
        return UserDetailedSchema(email=EmailStr(user.email),
                                  username=user.username,
                                  likes=likes,
                                  following=following,
                                  followers=followers, description=description,
                                  profile_url=profile.path if profile is not None else "",
                                  background_url=background.path if background is not None else "",
                                  firstname=firstname, lastname=lastname, is_partner=user.is_partner
                                  )
