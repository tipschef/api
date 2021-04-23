from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.user.model.user_model import UserModel
from app.user.schema.user_create_schema import UserCreateSchema


@dataclass
class UserRepository:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> UserModel:
        return db.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreateSchema) -> UserModel:
        fake_hashed_password = user.password + 'notreallyhashed'
        db_user = UserModel(email=user.email, password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
