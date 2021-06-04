from datetime import datetime
from typing import List, Optional

from app.recipe.model.recipe.recipe_model import RecipeModel
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_response_base_schema import RecipeResponseBaseSchema
from app.recipe.schema.step.step_schema import StepSchema


class RecipeResponseSchema(RecipeResponseBaseSchema):
    creator_id: int
    last_updated: Optional[datetime] = None
    created_at: Optional[datetime] = None

    @staticmethod
    def from_recipe_model(recipe: RecipeModel, steps: List[StepSchema], thumbnail: MediaSchema, video: MediaSchema):
        return RecipeResponseSchema(id=recipe.id,
                                    min_tier=recipe.min_tier,
                                    name=recipe.name,
                                    description=recipe.description,
                                    thumbnail=thumbnail,
                                    video=video,
                                    creator_id=recipe.creator_id,
                                    steps=steps,
                                    last_updated=recipe.last_updated,
                                    created_at=recipe.created_date)
