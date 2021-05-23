from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.repository.like_repository import LikeRepository
from app.user.schema.user_schema import UserSchema


@dataclass
class LikeService:

    @staticmethod
    def like_someone_by_id(database: Session, user: UserSchema, recipe_od: int) -> bool:
        if LikeRepository.get_like(database, recipe_od, user.id) is None:
            LikeRepository.like(database, recipe_od, user.id)
            return True
        return False

    @staticmethod
    def dislike_someone_by_id(database: Session, user: UserSchema, recipe_od: int) -> bool:
        if LikeRepository.get_like(database, recipe_od, user.id) is not None:
            LikeRepository.dislike(database, recipe_od, user.id)
            return True
        return False
