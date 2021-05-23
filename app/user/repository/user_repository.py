from dataclasses import dataclass
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.user.model.user_model import UserModel
from app.user.schema.user_create_schema import UserCreateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class UserRepository:

    @staticmethod
    def get_user_by_email(database: Session, email: str) -> Optional[UserModel]:
        return database.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[UserModel]:
        for database in get_database():
            return database.query(UserModel).filter(UserModel.username == username).first()

    @staticmethod
    def create_user(database: Session, user: UserCreateSchema) -> UserModel:
        hashed_password = user.password.get_secret_value()
        db_user = UserModel(email=user.email, password=pwd_context.hash(hashed_password), username=user.username)
        database.add(db_user)
        database.commit()
        database.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_id(database: Session, user_id: int) -> Optional[UserModel]:
        return database.query(UserModel).filter(UserModel.id == user_id).first()
