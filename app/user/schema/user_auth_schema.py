from pydantic import EmailStr

from app.user.model.user_model import UserModel
from app.user.schema.user_schema import UserSchema


class UserAuthSchema(UserSchema):
    is_admin: bool
    is_cook: bool
    sub_enabled: bool
    is_partner: bool
    is_highlighted: bool

    @staticmethod
    def from_user_model(user: UserModel):
        return UserAuthSchema(id=user.id, email=EmailStr(user.email), username=user.username, is_admin=user.is_admin,
                              is_cook=user.is_cook, sub_enabled=user.sub_enabled, is_partner=user.is_partner,
                              is_highlighted=user.is_highlighted)

    class Config:
        orm_mode = True
