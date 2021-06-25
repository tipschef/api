from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.recipe.exception.recipe_service_exceptions import WrongUserToDeleteComment
from app.recipe.repository.comment_repository import CommentRepository
from app.recipe.schema.comment.comment_input_schema import CommentInputSchema
from app.recipe.schema.comment.comment_output_base_schema import CommentOutputBaseSchema
from app.user.schema.user_schema import UserSchema


@dataclass
class CommentService:

    @staticmethod
    def get_comments_by_recipe_id(database: Session, recipe_id: int) -> List[CommentOutputBaseSchema]:
        return [CommentOutputBaseSchema.from_comment_tuple(comment[0], comment[1], comment[2]) for comment in CommentRepository.get_all_comment_from_recipe(database, recipe_id)]

    @staticmethod
    def delete_comment_by_id(database: Session, user: UserSchema, comment_id: int, recipe_id: int) -> bool:
        if CommentRepository.get_comment_by_id(database, comment_id, recipe_id).user_id != user.id:
            raise WrongUserToDeleteComment(comment_id)
        CommentRepository.delete_comment_by_id(database, user.id, comment_id, recipe_id)
        return True

    @staticmethod
    def create_comment_on_a_recipe(database: Session, user: UserSchema, comment: CommentInputSchema, recipe_id: int):
        CommentRepository.create_a_comment(database, comment, user.id, recipe_id)
