from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app.user.model.subscription_model import SubscriptionModel


@dataclass
class SubscriptionRepository:

    @staticmethod
    def get_subscription(database: Session, subscribed_id: int, subscriber_id: int) -> Optional[SubscriptionModel]:
        return database.query(SubscriptionModel).filter(SubscriptionModel.subscribed_id == subscribed_id,
                                                        SubscriptionModel.subscriber_id == subscriber_id).first()

    @staticmethod
    def get_count_subscriber_by_subscribed_id(database: Session, subscribed_id: int) -> int:
        return database.query(SubscriptionModel).filter(SubscriptionModel.subscribed_id == subscribed_id).count()

    @staticmethod
    def subscribe(database: Session, subscribed_id: int, subscriber_id: int, tier: int,
                  gifted_id: Optional[int] = None) -> SubscriptionModel:
        db_subscribe = SubscriptionModel(subscribed_id=subscribed_id, subscriber_id=subscriber_id, gifted_id=gifted_id,
                                         tier=tier)
        print(db_subscribe)
        database.add(db_subscribe)
        database.commit()
        database.refresh(db_subscribe)
        return db_subscribe

    @staticmethod
    def unsubscribe(database: Session, subscribed_id: int, subscriber_id: int) -> None:
        database.query(SubscriptionModel).filter(SubscriptionModel.subscribed_id == subscribed_id,
                                                 SubscriptionModel.subscriber_id == subscriber_id).delete()
        database.commit()
