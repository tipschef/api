from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.user.model.user_model import UserModel
from app.user.schema.user_create_schema import UserCreateSchema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class UserRepository:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> UserModel:
        return db.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreateSchema) -> UserModel:
        db_user = UserModel(email=user.email, password=pwd_context.hash(user.password.get_secret_value()))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
