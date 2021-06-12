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
                            portion_number=recipe.portion_number,
                            portion_unit=recipe.portion_unit,
                            preparation_hours=recipe.preparation_hours,
                            preparation_minutes=recipe.preparation_minutes,
                            cooking_hours=recipe.cooking_hours,
                            cooking_minutes=recipe.cooking_minutes,
                            resting_hours=recipe.resting_hours,
                            resting_minutes=recipe.resting_minutes,
                            difficulty=recipe.difficulty,
                            cost=recipe.cost,
                            name=recipe.name,
                            description=recipe.description,
                            recipe_category_id=recipe.recipe_category_id,
                            recipe_cooking_type_id=recipe.recipe_cooking_type_id,
                            steps=recipe.steps,
                            ingredients=recipe.ingredients,
                            creator_id=creator_id)
