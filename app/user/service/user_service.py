from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.user.exception.user_route_exceptions import UserAlreadyExistsException
from app.user.model.user_model import UserModel
from app.user.repository.user_repository import UserRepository
from app.user.schema.user_create_schema import UserCreateSchema


@dataclass
class UserService:

    @staticmethod
    def create_user(db: Session, user: UserCreateSchema) -> UserModel:
        db_user = UserRepository.get_user_by_email(db, email=user.email)
        if db_user:
            raise UserAlreadyExistsException(user.email)

        return UserRepository.create_user(db, user)
