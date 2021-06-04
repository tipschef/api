from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.recipe.schema.recipe.recipe_base_schema import RecipeBaseSchema


class RecipeSchema(RecipeBaseSchema):
    id: Optional[int]
    creator_id: int
    is_deleted: bool = False
    last_updated: Optional[datetime]
    created_at: Optional[datetime]

    @staticmethod
    def from_recipe_base_schema(recipe: RecipeBaseSchema, creator_id: int) -> RecipeSchema:
        return RecipeSchema(min_tier=recipe.min_tier,
                            name=recipe.name,
                            description=recipe.description,
                            steps=recipe.steps,
                            ingredients=recipe.ingredients,
                            creator_id=creator_id)
