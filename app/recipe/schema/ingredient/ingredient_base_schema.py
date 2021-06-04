from pydantic import BaseModel


class IngredientBaseSchema(BaseModel):
    ingredient_name: str
    ingredient_unit: str
    quantity: int
