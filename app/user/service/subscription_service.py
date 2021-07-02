import random
from dataclasses import dataclass
from datetime import datetime

from dateutil.relativedelta import relativedelta
from requests import Session

from app.payment.exception.payment_service_exceptions import NoPaymentMethodException
from app.payment.schema.payment_intent_schema import PaymentIntentSchema
from app.payment.service.payment_service import get_payment_service
from app.user.exception.subscription_service_exceptions import UserNotPartnerException, AlreadySubscribedToUser, \
    TierDoesNotExist, NotEnoughFollowersException, UserNotSubscribedException
from app.user.exception.user_route_exceptions import UsernameNotFoundException
from app.user.repository.follow_repository import FollowRepository
from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.tier_repository import TierRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.create_random_subscription_schema import CreateRandomSubscriptionSchema
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
    def gist_random_subscription(database: Session, user: UserSchema,
                                 create_random_subscription: CreateRandomSubscriptionSchema):
        user_to_be_subscribed = UserRepository.get_user_by_username(create_random_subscription.subscribed_username)

        if user_to_be_subscribed is None:
            raise UsernameNotFoundException(create_random_subscription.subscribed_username)
        if user_to_be_subscribed.is_partner is False:
            raise UserNotPartnerException(create_random_subscription.subscribed_username)

        followers = FollowRepository.get_followers_by_followed_id(database, user_to_be_subscribed.id)

        subscribers = SubscriptionRepository.get_ongoing_subscriber_by_subscribed_id(database, user_to_be_subscribed.id)

        if True not in [i.subscriber_id == user.id for i in subscribers]:
            raise UserNotSubscribedException(create_random_subscription.subscribed_username)
        not_subscribed_followers = []

        for follower in followers:
            if True not in [i.subscriber_id == follower.follower_id for i in subscribers]:
                not_subscribed_followers.append(follower)

        if len(not_subscribed_followers) < create_random_subscription.number:
            raise NotEnoughFollowersException()

        to_be_subscribed = random.sample(not_subscribed_followers, create_random_subscription.number)

        tier = TierRepository.get_tier(database, create_random_subscription.tier)

        if tier is None:
            raise TierDoesNotExist(str(create_random_subscription.tier))

        try:
            get_payment_service().create_payment_intent(database, user,
                                                        PaymentIntentSchema(amount=int(
                                                            tier.price * 100 * create_random_subscription.number)))
            date = datetime.today() + relativedelta(months=+1)
            for to_be_subscribed_user in to_be_subscribed:
                SubscriptionRepository.create_subscription(database, user_to_be_subscribed.id, to_be_subscribed_user.follower_id,
                                                           tier.tier, date, user.id)
        except NoPaymentMethodException:
            raise NoPaymentMethodException()

    @staticmethod
    def count_user_available_followers(database: Session, username: str) -> int:
        user = UserRepository.get_user_by_username(username)

        followers = FollowRepository.get_followers_by_followed_id(database, user.id)

        subscribers = SubscriptionRepository.get_ongoing_subscriber_by_subscribed_id(database, user.id)

        not_subscribed_followers = []

        for follower in followers:
            if True not in [i.subscriber_id == follower.follower_id for i in subscribers]:
                not_subscribed_followers.append(follower)

        return len(not_subscribed_followers)
