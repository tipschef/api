from app.user.schema.user_create_schema import UserCreateSchema


class UserUpdateSchema(UserCreateSchema):
    firstname: str
    lastname: str
    description: str
