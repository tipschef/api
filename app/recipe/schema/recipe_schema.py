from datetime import datetime

from app.recipe.model.recipe_model import RecipeModel
from app.recipe.schema.recipe_base_schema import RecipeBaseSchema


class RecipeSchema(RecipeBaseSchema):
    created_date: datetime
    creator_id: int

    @staticmethod
    def from_recipe_base_schema(recipe: RecipeBaseSchema, created_date: datetime, creator_id: int):
        return RecipeSchema(id=recipe.id,
                            min_tier=recipe.min_tier,
                            name=recipe.name,
                            description=recipe.description,
                            is_deleted=recipe.is_deleted,
                            thumbnail_id=recipe.thumbnail_id,
                            video_id=recipe.video_id,
                            steps=recipe.steps,
                            created_date=created_date,
                            creator_id=creator_id)

    @staticmethod
    def from_recipe_model(recipe: RecipeModel):
        return RecipeSchema(id=recipe.id,
                            min_tier=recipe.min_tier,
                            name=recipe.name,
                            description=recipe.description,
                            is_deleted=recipe.is_deleted,
                            thumbnail_id=recipe.thumbnail_id,
                            video_id=recipe.video_id,
                            steps=recipe.steps,
                            created_date=recipe.created_date,
                            creator_id=recipe.creator_id)
