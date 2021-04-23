from app.user.model.user_model import UserModel
from app.user.schema.user_base_schema import UserBaseSchema


class UserSchema(UserBaseSchema):
    id: int

    @staticmethod
    def from_user_model(user: UserModel):
        return UserSchema(id=user.id, email=user.email)

    class Config:
        orm_mode = True
