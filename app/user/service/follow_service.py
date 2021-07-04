from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.user.repository.follow_repository import FollowRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.follow_schema import FollowSchema
from app.user.schema.user.user_schema import UserSchema


@dataclass
class FollowService:

    @staticmethod
    def follow_someone_by_username(database: Session, user: UserSchema, user_to_follow_username: str) -> bool:

        user_to_follow_id = UserRepository.get_user_by_username(user_to_follow_username).id
        if FollowRepository.get_follow(database, user_to_follow_id, user.id) is None:
            FollowRepository.follow(database, user_to_follow_id, user.id)
            return True
        return False

    @staticmethod
    def unfollow_someone_by_username(database: Session, user: UserSchema, user_to_follow_username: str) -> bool:
        user_to_follow_id = UserRepository.get_user_by_username(user_to_follow_username).id
        if FollowRepository.get_follow(database, user_to_follow_id, user.id) is not None:
            FollowRepository.unfollow(database, user_to_follow_id, user.id)
            return True
        return False

    @staticmethod
    def get_my_follows(database: Session, user: UserSchema) -> List[FollowSchema]:
        return [FollowSchema(username=x[1].username, date=x[0].created_date, is_partner=x[1].is_partner) for x in FollowRepository.get_follow_by_follower_id(database, user.id)]
