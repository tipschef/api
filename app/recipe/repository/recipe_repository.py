from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.recipe.model.recipe_model import RecipeModel
from app.recipe.schema.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.recipe_schema import RecipeSchema


@dataclass
class RecipeRepository:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeSchema, video_id: int, thumbnail_id: int) -> RecipeModel:
        db_recipe = RecipeModel(min_tier=recipe.min_tier,
                                name=recipe.name,
                                description=recipe.description,
                                thumbnail_id=thumbnail_id,
                                video_id=video_id,
                                creator_id=recipe.creator_id)
        database.add(db_recipe)
        database.commit()
        database.refresh(db_recipe)
        return db_recipe

    @staticmethod
    def get_all_recipe_for_user(database: Session, user_id: int) -> List[RecipeModel]:
        return database.query(RecipeModel).filter(RecipeModel.creator_id == user_id, RecipeModel.is_deleted.is_(False)).all()

    @staticmethod
    def get_recipe_by_id(database: Session, recipe_id: int) -> Optional[RecipeModel]:
        return database.query(RecipeModel).filter(RecipeModel.id == recipe_id, RecipeModel.is_deleted.is_(False)).first()

    @staticmethod
    def delete_recipe_by_id(database: Session, recipe_id: int) -> None:
        database.query(RecipeModel).filter(RecipeModel.is_deleted.is_(False), RecipeModel.id == recipe_id).update({RecipeModel.is_deleted: True})
        database.commit()

    @staticmethod
    def update_recipe_by_id(database: Session, recipe_id: int, recipe: RecipeResponseSchema, ) -> None:
        database.query(RecipeModel).filter(RecipeModel.is_deleted.is_(False), RecipeModel.id == recipe_id)\
                                   .update({RecipeModel.name: recipe.name,
                                            RecipeModel.min_tier: recipe.min_tier,
                                            RecipeModel.description: recipe.description,
                                            RecipeModel.last_updated: datetime.utcnow(),
                                            RecipeModel.video_id: recipe.video.id,
                                            RecipeModel.thumbnail_id: recipe.thumbnail.id})
        database.commit()
