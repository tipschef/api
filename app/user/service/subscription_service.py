from dataclasses import dataclass
from datetime import datetime

from dateutil.relativedelta import relativedelta
from requests import Session

from app.payment.exception.payment_service_exceptions import NoPaymentMethodException
from app.payment.schema.payment_intent_schema import PaymentIntentSchema
from app.payment.service.payment_service import get_payment_service
from app.user.exception.subscription_service_exceptions import UserNotPartnerException, AlreadySubscribedToUser, \
    TierDoesNotExist
from app.user.exception.user_route_exceptions import UsernameNotFoundException
from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.tier_repository import TierRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.create_subscription_schema import CreateSubscriptionSchema
from app.user.schema.user.user_schema import UserSchema


@dataclass
class SubscriptionService:

    @staticmethod
    def subscribe_to_someone_by_username(database: Session, user: UserSchema,
                                         create_subscription: CreateSubscriptionSchema):

        user_to_be_subscribed = UserRepository.get_user_by_username(create_subscription.subscribed_username)
        if user_to_be_subscribed is None:
            raise UsernameNotFoundException(create_subscription.subscribed_username)
        if user_to_be_subscribed.is_partner is False:
            raise UserNotPartnerException(create_subscription.subscribed_username)
        on_going_subscription = SubscriptionRepository.get_ongoing_subscription(database, user_to_be_subscribed.id,
                                                                                user.id)
        if on_going_subscription is not None:
            raise AlreadySubscribedToUser(user_to_be_subscribed.username)

        tier = TierRepository.get_tier(database, create_subscription.tier)
        if tier is None:
            raise TierDoesNotExist(str(create_subscription.tier))

        try:
            get_payment_service().create_payment_intent(database, user,
                                                        PaymentIntentSchema(amount=int(
                                                            tier.price * 100 * create_subscription.number_month)))
            date = datetime.today() + relativedelta(months=+create_subscription.number_month)
            SubscriptionRepository.create_subscription(database, user_to_be_subscribed.id, user.id, tier.tier, date)
        except NoPaymentMethodException:
            raise NoPaymentMethodException()

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
