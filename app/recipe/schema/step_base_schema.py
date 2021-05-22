from pydantic import BaseModel


class StepBaseSchema(BaseModel):
    content: str
    order: int
