from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.orm import Session

from app.authentication.service.authentication_service import AuthenticationService
from app.recipe.repository.like_repository import LikeRepository
from app.user.exception.user_route_exceptions import UserAlreadyExistsException, UsernameAlreadyExistsException, \
    UserNotFoundException
from app.user.model.user_model import UserModel
from app.user.repository.follow_repository import FollowRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.user_auth_schema import UserAuthSchema
from app.user.schema.user_detailed_schema import UserDetailedSchema
from app.user.schema.user_create_schema import UserCreateSchema


@dataclass
class UserService:

    @staticmethod
    def create_user(database: Session, user: UserCreateSchema) -> UserModel:
        db_user = UserRepository.get_user_by_email(database, email=user.email)
        if db_user:
            raise UserAlreadyExistsException(user.email)

        db_user = UserRepository.get_user_by_username(username=user.username)
        if db_user:
            raise UsernameAlreadyExistsException(user.username)

        return UserRepository.create_user(database, user)

    @staticmethod
    async def get_current_active_user(
            current_user: UserAuthSchema = Depends(AuthenticationService.get_current_user)) -> UserAuthSchema:
        return current_user

    @staticmethod
    def get_user_by_username(database: Session, username: str) -> UserDetailedSchema:
        user = UserRepository.get_user_by_username(username)
        if user is None:
            raise UserNotFoundException(username)
        count_follower = FollowRepository.get_count_followers_by_followed_username(database, user.id)
        count_likes = LikeRepository.get_count_like_by_user_id(database, user.id)
        return UserDetailedSchema.from_user_model(user, count_likes, count_follower)
