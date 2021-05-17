from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.model.recipe_model import RecipeModel
from app.recipe.schema.recipe_schema import RecipeSchema


@dataclass
class RecipeRepository:

    @staticmethod
    def create_recipe(database: Session, recipe: RecipeSchema) -> RecipeModel:
        db_recipe = RecipeModel(id=recipe.id,
                                min_tier=recipe.min_tier,
                                name=recipe.name,
                                description=recipe.description,
                                is_deleted=recipe.is_deleted,
                                thumbnail_id=recipe.thumbnail_id,
                                video_id=recipe.video_id,
                                steps=recipe.steps,
                                created_date=recipe.created_date,
                                creator_id=recipe.creator_id)
        database.add(db_recipe)
        database.commit()
        database.refresh(db_recipe)
        return db_recipe
