from __future__ import annotations

from typing import List, Optional

from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.schema.ingredient.ingredient_base_schema import IngredientBaseSchema
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.step.step_schema import StepSchema


class RecipeResponseExtendedSchema(RecipeResponseSchema):
    can_be_seen: bool
    creator_username: str
    creator_icon: Optional[str]
    creator_is_partner: Optional[bool]

    @staticmethod
    def from_recipe_models_seen(recipe: RecipeModel, steps: List[StepSchema],
                                ingredients: List[IngredientBaseSchema], medias: List[MediaSchema],
                                thumbnail: MediaSchema, video: MediaSchema,
                                can_be_seen: bool, creator_username: str, creator_icon: str, creator_is_partner: bool) -> RecipeResponseExtendedSchema:
        return RecipeResponseExtendedSchema(min_tier=recipe.min_tier,
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
                                            id=recipe.id,
                                            last_updated=recipe.last_updated,
                                            created_date=recipe.created_date,
                                            steps=steps,
                                            ingredients=ingredients,
                                            medias=medias,
                                            thumbnail=thumbnail,
                                            video=video,
                                            creator_username=creator_username,
                                            creator_icon=creator_icon,
                                            creator_id=recipe.creator_id,
                                            creator_is_partner=creator_is_partner,
                                            can_be_seen=can_be_seen)
