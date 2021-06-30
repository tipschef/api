from dataclasses import dataclass

from requests import Session

from app.payment.schema.payment_intent_schema import PaymentIntentSchema
from app.payment.service.payment_service import get_payment_service
from app.user.exception.subscription_service_exceptions import UserNotPartnerException
from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.tier_repository import TierRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.user_schema import UserSchema


@dataclass
class SubscriptionService:

    @staticmethod
    def subscribe_to_someone_by_username(database: Session, user: UserSchema, user_to_be_subscribed_to_username: str,
                                         tier: int) -> bool:

        user_to_be_subscribed = UserRepository.get_user_by_username(user_to_be_subscribed_to_username)
        if user_to_be_subscribed.is_partner is False:
            raise UserNotPartnerException(user_to_be_subscribed_to_username)
        if SubscriptionRepository.get_subscription(database, user_to_be_subscribed.id, user.id) is None:
            tier = TierRepository.get_tier(database, tier)
            get_payment_service().create_payment_intent(database, user, PaymentIntentSchema(amount=int(tier.price * 100)))
            SubscriptionRepository.subscribe(database, user_to_be_subscribed.id, user.id, tier.tier)
            return True
        return False

    @staticmethod
    def unsubscribe_to_someone_by_username(database: Session, user: UserSchema,
                                           user_to_be_subscribed_to_username: str) -> bool:
        user_to_be_unsubscribed_id = UserRepository.get_user_by_username(user_to_be_subscribed_to_username).id
        if SubscriptionRepository.get_subscription(database, user_to_be_unsubscribed_id, user.id) is not None:
            SubscriptionRepository.unsubscribe(database, user_to_be_unsubscribed_id, user.id)
            return True
        return False

    @staticmethod
    def gift_a_subscription_to_someone_by_username(database: Session, user: UserSchema,
                                                   user_to_be_subscribed_to_username: str,
                                                   user_to_subscribe_to_username: str, tier: int) -> bool:

        user_to_be_subscribed = UserRepository.get_user_by_username(user_to_be_subscribed_to_username)
        user_to_subscribe_id = UserRepository.get_user_by_username(user_to_subscribe_to_username).id
        if user_to_be_subscribed.is_partner is False:
            raise UserNotPartnerException(user_to_be_subscribed_to_username)
        if SubscriptionRepository.get_subscription(database, user_to_be_subscribed.id, user.id) is None:
            SubscriptionRepository.subscribe(database, user_to_be_subscribed.id, user_to_subscribe_id, tier, user.id)
            return True
        return False
