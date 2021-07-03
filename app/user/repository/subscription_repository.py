from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app.user.model.subscription_model import SubscriptionModel


@dataclass
class SubscriptionRepository:

    @staticmethod
    def get_all_subscription_between_two_users(database: Session, subscribed_id: int, subscriber_id: int) -> List[SubscriptionModel]:
        return database.query(SubscriptionModel).filter(SubscriptionModel.subscribed_id == subscribed_id,
                                                        SubscriptionModel.subscriber_id == subscriber_id).all()

    @staticmethod
    def get_expired_subscriptions(database: Session, subscriber_id: int) -> List[SubscriptionModel]:
        return database.query(SubscriptionModel).filter(datetime.utcnow() > SubscriptionModel.date_end)\
            .filter(SubscriptionModel.subscriber_id == subscriber_id).all()

    @staticmethod
    def get_ongoing_subscription(database: Session, subscribed_id: int, subscriber_id: int) -> Optional[SubscriptionModel]:
        return database.query(SubscriptionModel).filter(SubscriptionModel.subscribed_id == subscribed_id,
                                                        SubscriptionModel.subscriber_id == subscriber_id) \
            .filter(datetime.utcnow() <= SubscriptionModel.date_end) \
            .filter(datetime.utcnow() >= SubscriptionModel.created_date) \
            .first()

    @staticmethod
    def get_count_subscriber_by_subscribed_id(database: Session, subscribed_id: int) -> int:
        return database.query(SubscriptionModel).filter(SubscriptionModel.subscribed_id == subscribed_id)\
            .filter(datetime.utcnow() <= SubscriptionModel.date_end) \
            .filter(datetime.utcnow() >= SubscriptionModel.created_date).count()

    @staticmethod
    def get_ongoing_subscriber_by_subscribed_id(database: Session, subscribed_id: int) -> List[SubscriptionModel]:
        return database.query(SubscriptionModel).filter(SubscriptionModel.subscribed_id == subscribed_id) \
            .filter(datetime.utcnow() <= SubscriptionModel.date_end) \
            .filter(datetime.utcnow() >= SubscriptionModel.created_date) \
            .all()

    @staticmethod
    def get_ongoing_subscriptions_by_subscriber_id(database: Session, subscriber_id: int) -> List[SubscriptionModel]:
        return database.query(SubscriptionModel).filter(SubscriptionModel.subscriber_id == subscriber_id) \
            .filter(datetime.utcnow() <= SubscriptionModel.date_end) \
            .filter(datetime.utcnow() >= SubscriptionModel.created_date) \
            .all()

    @staticmethod
    def get_given_ongoing_subscriptions_by_subscriber_id(database: Session, subscriber_id: int) -> List[SubscriptionModel]:
        return database.query(SubscriptionModel).filter(SubscriptionModel.subscriber_id == subscriber_id) \
            .filter(SubscriptionModel.gifted_id.isnot(None)) \
            .filter(datetime.utcnow() <= SubscriptionModel.date_end) \
            .filter(datetime.utcnow() >= SubscriptionModel.created_date) \
            .all()

    @staticmethod
    def create_subscription(database: Session, subscribed_id: int, subscriber_id: int, tier: int, date_end: datetime, number_month: int,
                            gifted_id: Optional[int] = None) -> SubscriptionModel:
        db_subscribe = SubscriptionModel(subscribed_id=subscribed_id, subscriber_id=subscriber_id, gifted_id=gifted_id,
                                         tier=tier, date_end=date_end, number_month=number_month)
        database.add(db_subscribe)
        database.commit()
        database.refresh(db_subscribe)
        return db_subscribe