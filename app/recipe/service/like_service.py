from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.repository.like_repository import LikeRepository
from app.recipe.schema.like.like_schema import LikeSchema
from app.user.schema.user.user_schema import UserSchema


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
    def get_like_by_recipe_id(database: Session, recipe_id: int, user: UserSchema) -> LikeSchema:
        like_count = LikeRepository.get_like(database, recipe_id)
        liked_by_me = LikeRepository.get_like_by_user(database, recipe_id, user.id) is not None
        return LikeSchema(recipe_id=recipe_id, like_count=like_count, liked_by_me=liked_by_me)
