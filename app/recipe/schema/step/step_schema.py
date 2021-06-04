from datetime import datetime
from typing import Optional

from app.recipe.model.step.step_model import StepModel
from app.recipe.schema.step.step_base_schema import StepBaseSchema


class StepSchema(StepBaseSchema):
    created_date: Optional[datetime]
    id: int

    @staticmethod
    def from_step_model(step_model: StepModel):
        return StepSchema(id=step_model.id,
                          created_date=step_model.created_date,
                          content=step_model.content,
                          order=step_model.order)
