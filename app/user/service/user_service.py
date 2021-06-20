from dataclasses import dataclass
from typing import List

from fastapi import Depends, UploadFile
from sqlalchemy.orm import Session

from app.authentication.service.authentication_service import AuthenticationService
from app.common.service.bucket_manager_service import get_bucket_manager_service
from app.recipe.repository.like_repository import LikeRepository
from app.recipe.repository.media.media_category_repository import MediaCategoryRepository
from app.recipe.repository.media.media_repository import MediaRepository
from app.recipe.repository.recipe.recipe_repository import RecipeRepository
from app.recipe.schema.media.media_base_schema import MediaBaseSchema
from app.recipe.schema.media.media_category_schema import MediaCategorySchema
from app.recipe.schema.media.media_schema import MediaSchema
from app.user.exception.user_route_exceptions import UserAlreadyExistsException, UsernameAlreadyExistsException, \
    UsernameNotFoundException, WrongUploadFileType, UserIdNotFoundException
from app.user.model.user_model import UserModel
from app.user.repository.follow_repository import FollowRepository
from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.user_auth_schema import UserAuthSchema
from app.user.schema.user_create_schema import UserCreateSchema
from app.user.schema.user_detailed_schema import UserDetailedSchema
from app.user.schema.user_schema import UserSchema


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
    def get_user_by_username(database: Session, username: str, current_user: UserSchema) -> UserDetailedSchema:
        user = UserRepository.get_user_by_username(username)
        if user is None:
            raise UsernameNotFoundException(username)

        if user.profile_media_id is not None:
            profile_media = MediaRepository.get_media_by_id(database, user.profile_media_id)
        else:
            profile_media = None

        if user.background_media_id is not None:
            background_media = MediaRepository.get_media_by_id(database, user.background_media_id)
        else:
            background_media = None

        follow = FollowRepository.get_follow(database, followed_id=user.id, follower_id=current_user.id)
        following = follow is not None

        count_follower = FollowRepository.get_count_followers_by_followed_username(database, user.id)
        count_likes = LikeRepository.get_count_like_by_user_id(database, user.id)

        return UserDetailedSchema.from_user_model_with_follow(user, count_likes, count_follower, user.description,
                                                              profile_media, background_media, following)

    @staticmethod
    def search_username(database: Session, username: str, current_user: UserSchema) -> List[UserDetailedSchema]:
        users = UserRepository.search_username(database, username)
        schema_to_return = []
        for user in users:
            if user.profile_media_id is not None:
                profile_media = MediaRepository.get_media_by_id(database, user.profile_media_id)
            else:
                profile_media = None

            if user.background_media_id is not None:
                background_media = MediaRepository.get_media_by_id(database, user.background_media_id)
            else:
                background_media = None

            follow = FollowRepository.get_follow(database, followed_id=user.id, follower_id=current_user.id)
            following = follow is not None

            count_follower = FollowRepository.get_count_followers_by_followed_username(database, user.id)
            count_likes = LikeRepository.get_count_like_by_user_id(database, user.id)
            count_subscriber = SubscriptionRepository.get_count_subscriber_by_subscribed_id(database, user.id)
            count_recipe = RecipeRepository.get_count_recipe_by_creator_id(database, user.id)
            schema_to_return.append(
                UserDetailedSchema.from_user_model_with_data(user, count_likes, count_follower, user.description,
                                                             profile_media, background_media, following,
                                                             subscribers=count_subscriber, recipes=count_recipe))

        return schema_to_return

    @staticmethod
    def get_user_by_user_id(database: Session, user_id: int) -> UserDetailedSchema:
        user = UserRepository.get_user_by_id(database, user_id)

        if user is None:
            raise UserIdNotFoundException(user_id)

        if user.profile_media_id is not None:
            profile_media = MediaRepository.get_media_by_id(database, user.profile_media_id)
        else:
            profile_media = None

        if user.background_media_id is not None:
            background_media = MediaRepository.get_media_by_id(database, user.background_media_id)
        else:
            background_media = None

        count_follower = FollowRepository.get_count_followers_by_followed_username(database, user.id)
        count_likes = LikeRepository.get_count_like_by_user_id(database, user.id)
        return UserDetailedSchema.from_user_model(user, count_likes, count_follower, user.description, profile_media,
                                                  background_media)

    @staticmethod
    def update_user_profile_picture(database: Session, creator_id: int, media: UploadFile) -> MediaSchema:
        media_category = MediaCategoryRepository.get_media_category_by_name(database, media.content_type.split('/')[0])

        creator = UserRepository.get_user_by_id(database, creator_id)
        if media.content_type.split('/')[0] != 'image':
            raise WrongUploadFileType

        if media_category is None:
            media_category = MediaCategoryRepository.create_media_category(database, MediaCategorySchema(
                name=media.content_type.split('/')[0], description=media.content_type.split('/')[0]))
        media_schema = MediaBaseSchema(path='temp', media_category_id=media_category.id)
        created_media = MediaRepository.create_media(database, media_schema)
        filename = get_bucket_manager_service().save_file(
            f'{creator_id}/profile/{created_media.id}_{media.filename}', media.file)
        created_media.path = filename
        MediaRepository.update_media_by_id(database, created_media.id, filename)

        MediaRepository.delete_media_by_id(database, creator.profile_media_id)

        UserRepository.update_profile_picture(database, creator_id, created_media.id)

        return MediaSchema.from_media_model(created_media)

    @staticmethod
    def update_user_background_picture(database: Session, creator_id: int, media: UploadFile) -> MediaSchema:
        media_category = MediaCategoryRepository.get_media_category_by_name(database, media.content_type.split('/')[0])

        creator = UserRepository.get_user_by_id(database, creator_id)
        if media.content_type.split('/')[0] != 'image':
            raise WrongUploadFileType

        if media_category is None:
            media_category = MediaCategoryRepository.create_media_category(database, MediaCategorySchema(
                name=media.content_type.split('/')[0], description=media.content_type.split('/')[0]))
        media_schema = MediaBaseSchema(path='temp', media_category_id=media_category.id)
        created_media = MediaRepository.create_media(database, media_schema)
        filename = get_bucket_manager_service().save_file(
            f'{creator_id}/background/{created_media.id}_{media.filename}', media.file)
        created_media.path = filename
        MediaRepository.update_media_by_id(database, created_media.id, filename)

        MediaRepository.delete_media_by_id(database, creator.background_media_id)

        UserRepository.update_background_picture(database, creator_id, created_media.id)

        return MediaSchema.from_media_model(created_media)
