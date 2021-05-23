from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app.recipe.model.like_model import LikeModel


@dataclass
class LikeRepository:

    @staticmethod
    def get_count_like_by_user_id(database: Session, user_id: int) -> int:
        return database.query(LikeModel).filter(LikeModel.user_id == user_id).count()

    @staticmethod
    def get_like(database: Session, recipe_id: int, user_id: int) -> Optional[LikeModel]:
        return database.query(LikeModel).filter(LikeModel.recipe_id == recipe_id, LikeModel.user_id == user_id).first()

    @staticmethod
    def like(database: Session, recipe_id: int, user_id: int) -> LikeModel:
        db_like = LikeModel(recipe_id=recipe_id, user_id=user_id)
        database.add(db_like)
        database.commit()
        database.refresh(db_like)
        return db_like

    @staticmethod
    def dislike(database: Session, recipe_id: int, user_id: int) -> None:
        database.query(LikeModel).filter(LikeModel.recipe_id == recipe_id, LikeModel.user_id == user_id).delete()
        database.commit()
