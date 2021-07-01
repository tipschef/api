from datetime import datetime

from pydantic import BaseModel

from app.recipe.model.comment_model import CommentModel
from app.recipe.model.media.media_model import MediaModel
from app.user.model.user_model import UserModel
from app.user.schema.user.user_shortened_schema import UserShortenedSchema


class CommentOutputBaseSchema(BaseModel):
    content: str
    id: int
    user: UserShortenedSchema
    recipe_id: int
    created_date: datetime

    @staticmethod
    def from_comment_tuple(comment: CommentModel, user: UserModel, media: MediaModel):
        return CommentOutputBaseSchema(content=comment.content,
                                       id=comment.id,
                                       user=UserShortenedSchema(username=user.username, profile_picture=media.path if media is not None else ''),
                                       recipe_id=comment.recipe_id,
                                       created_date=comment.created_date)
