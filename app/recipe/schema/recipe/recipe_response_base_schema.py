from typing import List

from pydantic import BaseModel

from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.step.step_schema import StepSchema


class RecipeResponseBaseSchema(BaseModel):
    id: int
    min_tier: int
    name: str
    description: str
    thumbnail: MediaSchema
    video: MediaSchema
    steps: List[StepSchema]
