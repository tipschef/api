from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.schema.media.media_schema import MediaSchema


class RecipeSimpleSchema(BaseModel):
    id: int
    name: str
    thumbnail: Optional[MediaSchema]

    @staticmethod
    def from_recipe_model(recipe: RecipeModel) -> RecipeSimpleSchema:
        return RecipeSimpleSchema(id=recipe.id,
                                  name=recipe.name)

    @staticmethod
    def from_recipe_model_with_thumbnail(recipe: RecipeModel, thumbnail: MediaSchema) -> RecipeSimpleSchema:
        return RecipeSimpleSchema(id=recipe.id,
                                  name=recipe.name,
                                  thumbnail=thumbnail)