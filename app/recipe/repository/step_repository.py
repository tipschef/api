from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.recipe.model.step_model import StepModel
from app.recipe.schema.step_schema import StepSchema


@dataclass
class StepRepository:

    @staticmethod
    def create_step(database: Session, step: StepSchema, recipe_id: int) -> StepModel:
        db_step = StepModel(content=step.description, is_deleted=False, recipe_id=recipe_id,
                            created_date=datetime.now())
        database.add(db_step)
        database.commit()
        database.refresh(db_step)
        return db_step

    @staticmethod
    def create_steps(database: Session, steps: List[StepSchema], recipe_id: int) -> List[StepSchema]:
        db_step_list = [StepModel(content=step.description, is_deleted=False, recipe_id=recipe_id,
                                  created_date=datetime.now()) for step in steps]
        database.bulk_save_objects(db_step_list)
        database.commit()
        database.refresh(db_step_list)
        return db_step_list
