from pydantic import BaseModel


class StepSchema(BaseModel):
    id_step: int
    description: str