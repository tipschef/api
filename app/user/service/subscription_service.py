from dataclasses import dataclass

from requests import Session

from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.user_schema import UserSchema


@dataclass
class SubscriptionService:

    @staticmethod
    def subscribe_to_someone_by_username(database: Session, user: UserSchema, user_to_be_subscribed_to_username: str, tier: int) -> bool:

        user_to_be_subscribed_id = UserRepository.get_user_by_username(user_to_be_subscribed_to_username).id
        if SubscriptionRepository.get_subscription(database, user_to_be_subscribed_id, user.id) is None:
            SubscriptionRepository.subscribe(database, user_to_be_subscribed_id, user.id, tier)
            return True
        return False

    @staticmethod
    def unsubscribe_to_someone_by_username(database: Session, user: UserSchema, user_to_be_subscribed_to_username: str) -> bool:
        user_to_be_unsubscribed_id = UserRepository.get_user_by_username(user_to_be_subscribed_to_username).id
        if SubscriptionRepository.get_subscription(database, user_to_be_unsubscribed_id, user.id) is not None:
            SubscriptionRepository.unsubscribe(database, user_to_be_unsubscribed_id, user.id)
            return True
        return False

    @staticmethod
    def gift_a_subscription_to_someone_by_username(database: Session, user: UserSchema, user_to_be_subscribed_to_username: str,
                                         user_to_subscribe_to_username: str, tier: int) -> bool:

        user_to_be_subscribed_id = UserRepository.get_user_by_username(user_to_be_subscribed_to_username).id
        user_to_subscribe_id = UserRepository.get_user_by_username(user_to_subscribe_to_username).id
        if SubscriptionRepository.get_subscription(database, user_to_be_subscribed_id, user.id) is None:
            SubscriptionRepository.subscribe(database, user_to_be_subscribed_id, user_to_subscribe_id, tier, user.id)
            return True
        return False
