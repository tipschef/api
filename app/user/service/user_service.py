from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.orm import Session

from app.authentication.schema.authentication_schema import AuthenticationSchema
from app.authentication.service.authentication_service import AuthenticationService
from app.user.exception.user_route_exceptions import UserAlreadyExistsException
from app.user.model.user_model import UserModel
from app.user.repository.user_repository import UserRepository
from app.user.schema.user_create_schema import UserCreateSchema
from app.user.schema.user_schema import UserSchema


@dataclass
class UserService:

    @staticmethod
    def create_user(database: Session, user: UserCreateSchema) -> UserModel:
        db_user = UserRepository.get_user_by_email(database, email=user.email)
        if db_user:
            raise UserAlreadyExistsException(user.email)

        return UserRepository.create_user(database, user)

    @staticmethod
    async def get_current_active_user(current_user: UserSchema = Depends(AuthenticationService.get_current_user)) -> UserSchema:
        return current_user
