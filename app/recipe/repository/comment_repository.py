from dataclasses import dataclass
from typing import List, Tuple

from sqlalchemy.orm import Session

from app.recipe.model.comment_model import CommentModel
from app.recipe.model.media.media_model import MediaModel
from app.recipe.schema.comment.comment_input_schema import CommentInputSchema
from app.user.model.user_model import UserModel


@dataclass
class CommentRepository:

    @staticmethod
    def create_a_comment(database: Session, comment: CommentInputSchema, user_id: int, recipe_id: int) -> CommentModel:
        db_comment = CommentModel(content=comment.content, recipe_id=recipe_id, user_id=user_id)
        database.add(db_comment)
        database.commit()
        database.refresh(db_comment)
        return db_comment

    @staticmethod
    def get_all_comment_from_recipe(database: Session, recipe_id: int) -> List[Tuple[CommentModel, UserModel, MediaModel]]:
        return database.query(CommentModel, UserModel, MediaModel) \
            .join(UserModel, UserModel.id == CommentModel.user_id) \
            .join(MediaModel, MediaModel.id == UserModel.profile_media_id) \
            .filter(CommentModel.recipe_id == recipe_id) \
            .filter(CommentModel.is_deleted == False) \
            .order_by(CommentModel.created_date.desc())\
            .all()

    @staticmethod
    def delete_comment_by_id(database: Session, user_id: int, comment_id: int, recipe_id: int) -> None:
        database.query(CommentModel).filter(CommentModel.is_deleted.is_(False)) \
                .filter(CommentModel.user_id == user_id)\
                .filter(CommentModel.id == comment_id)\
                .filter(CommentModel.recipe_id == recipe_id)\
                .update({CommentModel.is_deleted: True})
        database.commit()

    @staticmethod
    def get_comment_by_id(database: Session, comment_id: int, recipe_id: int) -> CommentModel:
        return database.query(CommentModel) \
            .filter(CommentModel.id == comment_id) \
            .filter(CommentModel.recipe_id == recipe_id) \
            .filter(CommentModel.is_deleted == False) \
            .first()
