from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.model.ingredient.ingredient_unit_model import IngredientUnitModel


@dataclass
class IngredientUnitRepository:
    @staticmethod
    def get_ingredient_unit_by_name(database: Session, ingredient_unit_name: str) -> IngredientUnitModel:
        return database.query(IngredientUnitModel).filter(IngredientUnitModel.name == ingredient_unit_name).first()

    @staticmethod
    def create_ingredient_unit(database: Session, name: str) -> IngredientUnitModel:
        db_ingredient_unit = IngredientUnitModel(name=name)
        database.add(db_ingredient_unit)
        database.commit()
        database.refresh(db_ingredient_unit)
        return db_ingredient_unit
