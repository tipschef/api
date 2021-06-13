from datetime import datetime
from typing import List, Optional

from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.schema.ingredient.ingredient_base_schema import IngredientBaseSchema
from app.recipe.schema.recipe.recipe_response_base_schema import RecipeResponseBaseSchema
from app.recipe.schema.step.step_schema import StepSchema


class RecipeResponseSchema(RecipeResponseBaseSchema):
    creator_id: int
    last_updated: Optional[datetime] = None
    created_at: Optional[datetime] = None

    @staticmethod
    def from_recipe_model(recipe: RecipeModel, steps: List[StepSchema], ingredients: List[IngredientBaseSchema]):
        return RecipeResponseSchema(id=recipe.id,
                                    min_tier=recipe.min_tier,
                                    name=recipe.name,
                                    description=recipe.description,
                                    creator_id=recipe.creator_id,
                                    steps=steps,
                                    ingredients=ingredients,
                                    last_updated=recipe.last_updated,
                                    created_at=recipe.created_date)
