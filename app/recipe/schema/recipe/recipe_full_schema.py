from __future__ import annotations

from typing import List

from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.schema.ingredient.ingredient_base_schema import IngredientBaseSchema
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_schema import RecipeSchema
from app.recipe.schema.step.step_schema import StepSchema


class RecipeFullSchema(RecipeSchema):
    medias: List[MediaSchema]

    @staticmethod
    def from_recipe_models(recipe: RecipeModel, steps: List[StepSchema],
                          ingredients: List[IngredientBaseSchema], medias: List[MediaSchema]) -> RecipeFullSchema:
        return RecipeFullSchema(min_tier=recipe.min_tier,
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
                                medias=medias,
                                creator_id=recipe.creator_id)
