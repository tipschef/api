from dataclasses import dataclass
from typing import Optional, List

from sqlalchemy.orm import Session

from app.recipe.model.like_model import LikeModel
from app.recipe.model.recipe.recipe_model import RecipeModel


@dataclass
class LikeRepository:

    @staticmethod
    def get_count_like_by_user_id(database: Session, user_id: int) -> int:
        return database.query(LikeModel, RecipeModel)\
                       .filter(RecipeModel.creator_id == user_id)\
                       .filter(RecipeModel.id == LikeModel.recipe_id)\
                       .count()

    @staticmethod
    def get_like_by_user(database: Session, recipe_id: int, user_id: int) -> Optional[LikeModel]:
        return database.query(LikeModel).filter(LikeModel.recipe_id == recipe_id, LikeModel.user_id == user_id).first()

    @staticmethod
    def get_likes_by_user(database: Session, user_id: int, per_page: int, page: int) -> List[LikeModel]:
        return database.query(LikeModel).filter(LikeModel.user_id == user_id)\
                                        .order_by(LikeModel.created_date.desc())\
                                        .limit(per_page)\
                                        .offset((page - 1) * per_page)\
                                        .all()

    @staticmethod
    def get_like(database: Session, recipe_id: int) -> int:
        return database.query(LikeModel).filter(LikeModel.recipe_id == recipe_id).count()

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
