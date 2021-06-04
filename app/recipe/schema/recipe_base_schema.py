from typing import List

from pydantic import BaseModel

from app.recipe.schema.ingredient_base_schema import IngredientBaseSchema
from app.recipe.schema.step_base_schema import StepBaseSchema


class RecipeBaseSchema(BaseModel):
    min_tier: int
    name: str
    description: str
    steps: List[StepBaseSchema]
    ingredients: List[IngredientBaseSchema]
