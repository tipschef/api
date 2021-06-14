from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from app.recipe.model.step.step_model import StepModel
from app.recipe.schema.step.step_base_schema import StepBaseSchema
from app.recipe.schema.step.step_schema import StepSchema


@dataclass
class StepRepository:

    @staticmethod
    def create_step(database: Session, step: StepSchema, recipe_id: int) -> StepModel:
        db_step = StepModel(content=step.content, recipe_id=recipe_id, created_date=datetime.now(), order=step.order)
        database.add(db_step)
        database.commit()
        database.refresh(db_step)
        return db_step

    @staticmethod
    def create_steps(database: Session, steps: List[StepBaseSchema], recipe_id: int) -> None:
        db_step_list = [StepModel(content=step.content, recipe_id=recipe_id, order=step.order) for step in steps]
        database.bulk_save_objects(db_step_list)
        database.commit()

    @staticmethod
    def get_steps_by_recipe_id(database: Session, recipe_id: int) -> List[StepModel]:
        return database.query(StepModel).filter(StepModel.is_deleted.is_(False), StepModel.recipe_id == recipe_id).all()

    @staticmethod
    def delete_step_by_id(database: Session, step_id: int) -> None:
        database.query(StepModel).filter(StepModel.is_deleted.is_(False), StepModel.id == step_id).update(
            {StepModel.is_deleted: True})
        database.commit()

    @staticmethod
    def delete_multiple_steps(database: Session, steps: List[StepModel]) -> None:
        _ = [StepRepository.delete_step_by_id(database, step.id) for step in steps]
