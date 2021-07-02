import random
from dataclasses import dataclass
from datetime import datetime
from typing import List

from dateutil.relativedelta import relativedelta
from requests import Session

from app.payment.schema.payment_intent_schema import PaymentIntentSchema
from app.payment.service.payment_service import get_payment_service
from app.recipe.repository.media.media_repository import MediaRepository
from app.user.exception.subscription_service_exceptions import UserNotPartnerException, AlreadySubscribedToUser, \
    TierDoesNotExist, NotEnoughFollowersException, UserNotSubscribedException
from app.user.exception.user_route_exceptions import UsernameNotFoundException
from app.user.repository.follow_repository import FollowRepository
from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.tier_repository import TierRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.create_random_subscription_schema import CreateRandomSubscriptionSchema
from app.user.schema.create_subscription_schema import CreateSubscriptionSchema
from app.user.schema.get_subscription_schema import GetSubscriptionSchema
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

        get_payment_service().create_payment_intent(database, user,
                                                    PaymentIntentSchema(amount=int(
                                                        tier.price * 100 * create_subscription.number_month)))
        date = datetime.today() + relativedelta(months=+create_subscription.number_month)
        SubscriptionRepository.create_subscription(database, user_to_be_subscribed.id, user.id, tier.tier, date)

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

        get_payment_service().create_payment_intent(database, user,
                                                    PaymentIntentSchema(amount=int(
                                                        tier.price * 100 * create_random_subscription.number)))
        date = datetime.today() + relativedelta(months=+1)
        for to_be_subscribed_user in to_be_subscribed:
            SubscriptionRepository.create_subscription(database, user_to_be_subscribed.id, to_be_subscribed_user.follower_id,
                                                       tier.tier, date, user.id)

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

    @staticmethod
    def get_ongoing_subscriptions(database: Session, current_user: UserSchema) -> List[GetSubscriptionSchema]:
        ongoing_subscriptions = SubscriptionRepository.get_ongoing_subscriptions_by_subscriber_id(database,
                                                                                                  current_user.id)
        subscription_schema = []

        for subscription in ongoing_subscriptions:
            subscriptions = SubscriptionRepository.get_all_subscription_between_two_users(database,
                                                                                          subscription.subscribed_id,
                                                                                          subscriber_id=subscription.subscriber_id)
            total_month = sum(sub.number_month for sub in subscriptions)
            ongoing = SubscriptionRepository.get_ongoing_subscription(database, subscription.subscribed_id, subscriber_id=subscription.subscriber_id)
            total_month -= (ongoing.date_end.year - datetime.utcnow().year) * 12 + (ongoing.date_end.month - datetime.utcnow().month)

            subscribed = UserRepository.get_user_by_id(subscription.subscribed_id)

            if subscribed.profile_media_id is not None:
                profile_media = MediaRepository.get_media_by_id(database, subscribed.profile_media_id).path
            else:
                profile_media = None

            if subscribed.background_media_id is not None:
                background_media = MediaRepository.get_media_by_id(database, subscribed.background_media_id).path
            else:
                background_media = None

            subscription_schema.append(
                GetSubscriptionSchema.from_model(subscription, total_month, subscribed.username, profile_media,
                                                 background_media))

        return subscription_schema

    @staticmethod
    def get_gifted_subscriptions(database: Session, current_user: UserSchema) -> List[GetSubscriptionSchema]:
        ongoing_subscriptions = SubscriptionRepository.get_given_ongoing_subscriptions_by_subscriber_id(database,
                                                                                                        current_user.id)
        subscription_schema = []

        for subscription in ongoing_subscriptions:
            subscriptions = SubscriptionRepository.get_all_subscription_between_two_users(database,
                                                                                          subscription.subscribed_id,
                                                                                          subscriber_id=subscription.subscriber_id)
            total_month = sum(sub.number_month for sub in subscriptions)
            ongoing = SubscriptionRepository.get_ongoing_subscription(database, subscription.subscribed_id,
                                                                      subscriber_id=subscription.subscriber_id)
            total_month -= (ongoing.date_end.year - datetime.utcnow().year) * 12 + (
                        ongoing.date_end.month - datetime.utcnow().month)

            subscribed = UserRepository.get_user_by_id(subscription.subscribed_id)

            giver = UserRepository.get_user_by_id(subscription.gifted_id)

            if subscribed.profile_media_id is not None:
                profile_media = MediaRepository.get_media_by_id(database, subscribed.profile_media_id).path
            else:
                profile_media = None

            if subscribed.background_media_id is not None:
                background_media = MediaRepository.get_media_by_id(database, subscribed.background_media_id).path
            else:
                background_media = None

            subscription_schema.append(
                GetSubscriptionSchema.from_model_with_giver(subscription, total_month, subscribed.username,
                                                            profile_media,
                                                            background_media, giver.username))

        return subscription_schema

    @staticmethod
    def get_expired_subscriptions(database: Session, current_user: UserSchema) -> List[GetSubscriptionSchema]:
        ongoing_subscriptions = SubscriptionRepository.get_ongoing_subscriptions_by_subscriber_id(database,
                                                                                                  current_user.id)
        subscribed_ongoing_id = [i.subscribed_id for i in ongoing_subscriptions]
        all_expired_subscription = SubscriptionRepository.get_expired_subscriptions(database, current_user.id)

        expired_subscription = []

        for expired in all_expired_subscription:
            if expired.subscribed_id not in [i.subscribed_id for i in
                                             expired_subscription] and expired.subscribed_id not in subscribed_ongoing_id:
                expired_subscription.append(expired)

        subscription_schema = []

        for subscription in expired_subscription:
            subscriptions = SubscriptionRepository.get_all_subscription_between_two_users(database,
                                                                                          subscription.subscribed_id,
                                                                                          subscriber_id=subscription.subscriber_id)
            total_month = sum(sub.number_month for sub in subscriptions)

            subscribed = UserRepository.get_user_by_id(subscription.subscribed_id)

            if subscribed.profile_media_id is not None:
                profile_media = MediaRepository.get_media_by_id(database, subscribed.profile_media_id).path
            else:
                profile_media = None

            if subscribed.background_media_id is not None:
                background_media = MediaRepository.get_media_by_id(database, subscribed.background_media_id).path
            else:
                background_media = None

            subscription_schema.append(
                GetSubscriptionSchema.from_model(subscription, total_month, subscribed.username,
                                                 profile_media,
                                                 background_media))

        return subscription_schema
