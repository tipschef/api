from dataclasses import dataclass
from typing import Optional, List, Tuple

from sqlalchemy.orm import Session

from app.user.model.follow_model import FollowModel
from app.user.model.user_model import UserModel


@dataclass
class FollowRepository:

    @staticmethod
    def get_count_followers_by_followed_id(database: Session, followed_id: int) -> int:
        return database.query(FollowModel).filter(FollowModel.followed_id == followed_id).count()

    @staticmethod
    def get_followers_by_followed_id(database: Session, followed_id: int) -> List[FollowModel]:
        return database.query(FollowModel).filter(FollowModel.followed_id == followed_id).all()

    @staticmethod
    def get_follow(database: Session, followed_id: int, follower_id: int) -> Optional[FollowModel]:
        return database.query(FollowModel).filter(FollowModel.followed_id == followed_id,
                                                  FollowModel.follower_id == follower_id).first()

    @staticmethod
    def follow(database: Session, followed_id: int, follower_id: int) -> FollowModel:
        db_follow = FollowModel(followed_id=followed_id, follower_id=follower_id)
        database.add(db_follow)
        database.commit()
        database.refresh(db_follow)
        return db_follow

    @staticmethod
    def unfollow(database: Session, followed_id: int, follower_id: int) -> None:
        database.query(FollowModel).filter(FollowModel.followed_id == followed_id,
                                           FollowModel.follower_id == follower_id).delete()
        database.commit()

    @staticmethod
    def get_follow_by_follower_id(database: Session, follower_id: int) -> List[Tuple[FollowModel, UserModel]]:
        return database.query(FollowModel, UserModel)\
            .join(UserModel, UserModel.id == FollowModel.followed_id)\
            .filter(FollowModel.follower_id == follower_id) \
            .order_by(FollowModel.created_date.desc()) \
            .all()
