from pydantic import BaseModel


class UserShortenedSchema(BaseModel):
    username: str
    profile_picture: str
