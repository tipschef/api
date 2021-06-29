from __future__ import annotations

from pydantic.main import BaseModel


class RecipeTemplateSchema(BaseModel):
    recipe_id: int
    template_path: str
    recipe_name: str
    thumbnail_path: str
    portion_number: str
    portion_unit: str
    total_time: str
    ingredient_list: str
    instruction_list: str
