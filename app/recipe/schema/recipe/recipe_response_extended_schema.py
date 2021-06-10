from typing import List

from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_response_schema import RecipeResponseSchema
from app.recipe.schema.step.step_schema import StepSchema


class RecipeResponseExtendedSchema(RecipeResponseSchema):
    can_be_seen: bool

    @staticmethod
    def from_recipe_model(recipe: RecipeModel, steps: List[StepSchema], thumbnail: MediaSchema, video: MediaSchema,
                          can_be_seen: bool):
        return RecipeResponseExtendedSchema(id=recipe.id,
                                            min_tier=recipe.min_tier,
                                            name=recipe.name,
                                            description=recipe.description,
                                            thumbnail=thumbnail,
                                            video=video,
                                            creator_id=recipe.creator_id,
                                            steps=steps,
                                            last_updated=recipe.last_updated,
                                            created_at=recipe.created_date,
                                            can_be_seen=can_be_seen)
