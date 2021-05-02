from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app.user.model.user_model import UserModel
from app.user.schema.user_create_schema import UserCreateSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class UserRepository:

    @staticmethod
    def get_user_by_email(database: Session, email: str) -> Optional[UserModel]:
        return database.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def get_user_by_username(database: Session, username: str) -> Optional[UserModel]:
        return database.query(UserModel).filter(UserModel.username == username).first()

    @staticmethod
    def create_user(database: Session, user: UserCreateSchema) -> UserModel:
        hashed_password = user.password.get_secret_value()
        db_user = UserModel(email=user.email, password=pwd_context.hash(hashed_password))
        database.add(db_user)
        database.commit()
        database.refresh(db_user)
        return db_user
