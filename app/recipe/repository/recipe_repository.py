from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.recipe.model.recipe_model import RecipeModel
from app.recipe.schema.recipe_schema import RecipeSchema


@dataclass
class RecipeRepository:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeSchema, video_id: int, thumbnail_id: int) -> RecipeModel:
        db_recipe = RecipeModel(id=recipe.id,
                                min_tier=recipe.min_tier,
                                name=recipe.name,
                                description=recipe.description,
                                is_deleted=recipe.is_deleted,
                                thumbnail_id=thumbnail_id,
                                video_id=video_id,
                                steps=recipe.steps,
                                creator_id=recipe.creator_id)
        database.add(db_recipe)
        database.commit()
        database.refresh(db_recipe)
        return db_recipe

    @staticmethod
    def get_all_recipe_for_user(database: Session, user_id: int) -> List[RecipeModel]:
        return database.query(RecipeModel).filter(RecipeModel.creator_id == user_id).all()
