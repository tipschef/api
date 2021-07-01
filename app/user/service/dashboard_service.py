from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.repository.like_repository import LikeRepository
from app.user.model.dashboard_model import DashboardModel
from app.user.repository.dashboard_repository import DashboardRepository
from app.user.repository.follow_repository import FollowRepository
from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.dashboard_schema import DashboardSchema
from app.user.schema.user_schema import UserSchema


@dataclass
class DashboardService:

    @staticmethod
    def get_dashboard_data(database: Session, user: UserSchema):
        elements = DashboardRepository.get_dashboard_from_partner(database, user.id)
        return [DashboardSchema.from_model(x) for x in elements]

    @staticmethod
    def create_dashboard_data():
        for database in get_database():
            for user in UserRepository.get_partners(database):
                like = LikeRepository.get_count_like_by_user_id(database, user.id)
                sub = SubscriptionRepository.get_count_subscriber_by_subscribed_id(database, user.id)
                follower = FollowRepository.get_count_followers_by_followed_id(database, user.id)
                dashboard_element = DashboardModel(user_id=user.id, sub=sub, like=like, follower=follower)
                DashboardRepository.create_entry(database, dashboard_element)
