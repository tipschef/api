from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.repository.like_repository import LikeRepository
from app.user.schema.user_schema import UserSchema


@dataclass
class LikeService:

    @staticmethod
    def like_someone_by_id(database: Session, user: UserSchema, recipe_id: int) -> bool:
        if LikeRepository.get_like_by_user(database, recipe_id, user.id) is None:
            LikeRepository.like(database, recipe_id, user.id)
            return True
        return False

    @staticmethod
    def dislike_someone_by_id(database: Session, user: UserSchema, recipe_id: int) -> bool:
        if LikeRepository.get_like_by_user(database, recipe_id, user.id) is not None:
            LikeRepository.dislike(database, recipe_id, user.id)
            return True
        return False

    @staticmethod
    def get_like_by_recipe_id(database: Session, recipe_id: int):
        return LikeRepository.get_like(database, recipe_id)
