from typing import List

from pydantic import BaseModel

from app.recipe.schema.media_schema import MediaSchema
from app.recipe.schema.step_schema import StepSchema


class RecipeBaseSchema(BaseModel):
    id: int
    min_tier: int
    name: str
    description: str
    is_deleted: bool
    thumbnail: MediaSchema
    video: MediaSchema
    steps: List[StepSchema]
