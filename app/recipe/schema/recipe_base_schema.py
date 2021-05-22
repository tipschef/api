from typing import List

from pydantic import BaseModel

from app.recipe.schema.media_base_schema import MediaBaseSchema
from app.recipe.schema.step_base_schema import StepBaseSchema


class RecipeBaseSchema(BaseModel):
    min_tier: int
    name: str
    description: str
    thumbnail: MediaBaseSchema
    video: MediaBaseSchema
    steps: List[StepBaseSchema]
