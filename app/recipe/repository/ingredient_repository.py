from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.recipe.model.ingredient_model import IngredientModel


@dataclass
class IngredientRepository:
    @staticmethod
    def get_ingredient_by_name(database: Session, ingredient_name: str) -> IngredientModel:
        return database.query(IngredientModel).filter(IngredientModel.is_deleted.is_(False),
                                                      IngredientModel.name == ingredient_name).first()

    @staticmethod
    def create_ingredient(database: Session, name: str) -> IngredientModel:
        db_ingredient = IngredientModel(name=name)
        database.add(db_ingredient)
        database.commit()
        database.refresh(db_ingredient)
        return db_ingredient
