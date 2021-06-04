from typing import List

from pydantic import BaseModel

from app.recipe.schema.ingredient.ingredient_base_schema import IngredientBaseSchema
from app.recipe.schema.step.step_base_schema import StepBaseSchema


class RecipeBaseSchema(BaseModel):
    min_tier: int
    portion_number: int
    portion_unit: str
    preparation_hours: int
    preparation_minutes: int
    cooking_hours: int
    cooking_minutes: int
    resting_hours: int
    resting_minutes: int
    difficulty: int
    cost: int
    name: str
    description: str
    recipe_category_id: int
    recipe_cooking_type_id: int
    steps: List[StepBaseSchema]
    ingredients: List[IngredientBaseSchema]
