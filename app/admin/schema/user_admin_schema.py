from __future__ import annotations

from pydantic import BaseModel

from app.user.model.user_model import UserModel


class UserAdminSchema(BaseModel):
    id: int
    email: str
    username: str
    is_admin: bool
    is_partner: bool
    is_highlighted: bool
    bank_information_is_filled: bool

    @staticmethod
    def from_model(user: UserModel, bank_information_is_filled: bool) -> UserAdminSchema:
        return UserAdminSchema(id=user.id, email=user.email,
                               username=user.username,
                               is_admin=user.is_admin,
                               is_partner=user.is_partner,
                               is_highlighted=user.is_highlighted,
                               bank_information_is_filled=bank_information_is_filled)
