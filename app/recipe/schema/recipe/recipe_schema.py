from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.schema.ingredient.ingredient_base_schema import IngredientBaseSchema
from app.recipe.schema.recipe.recipe_base_schema import RecipeBaseSchema
from app.recipe.schema.step.step_schema import StepSchema


class RecipeSchema(RecipeBaseSchema):
    id: Optional[int]
    creator_id: int
    is_deleted: bool = False
    last_updated: Optional[datetime]
    created_date: Optional[datetime]

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

    @staticmethod
    def from_recipe_model(recipe: RecipeModel, steps: List[StepSchema], ingredients: List[IngredientBaseSchema]) -> RecipeSchema:
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
                            steps=steps,
                            ingredients=ingredients,
                            creator_id=recipe.creator_id)
