from dataclasses import dataclass

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.user.model.user_model import UserModel
from app.user.schema.user_create_schema import UserCreateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class UserRepository:

    @staticmethod
    def get_user_by_email(database: Session, email: str) -> UserModel:
        return database.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def create_user(database: Session, user: UserCreateSchema) -> UserModel:
        db_user = UserModel(email=user.email, password=pwd_context.hash(user.password.get_secret_value()))
        database.add(db_user)
        database.commit()
        database.refresh(db_user)
        return db_user
