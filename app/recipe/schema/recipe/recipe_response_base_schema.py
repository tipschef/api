from typing import List, Optional

from pydantic import BaseModel

from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.step.step_schema import StepSchema


class RecipeResponseBaseSchema(BaseModel):
    id: int
    min_tier: int
    name: str
    description: str
    thumbnail: Optional[MediaSchema]
    video: Optional[MediaSchema]
    steps: List[StepSchema]
