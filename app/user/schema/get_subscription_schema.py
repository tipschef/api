from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.user.model.subscription_model import SubscriptionModel


class GetSubscriptionSchema(BaseModel):
    tier: Optional[int]
    total_month: int
    subscribed_id: int
    subscribed_icon: Optional[str]
    subscribed_username: str
    subscribed_background: Optional[str]
    date_end: datetime
    giver_id: Optional[str]
    giver_username: Optional[str]

    @staticmethod
    def from_model(subscription: SubscriptionModel, total_month: int, subscribed_username: str, subscribed_icon: str,
                   subscribed_background: str) -> GetSubscriptionSchema:
        return GetSubscriptionSchema(
            tier=subscription.tier,
            date_end=subscription.date_end,
            subscribed_id=subscription.subscribed_id,
            total_month=total_month,
            subscribed_username=subscribed_username,
            subscribed_icon=subscribed_icon,
            subscribed_background=subscribed_background,
        )

    @staticmethod
    def from_model_with_giver(subscription: SubscriptionModel, total_month: int, subscribed_username: str,
                              subscribed_icon: str,
                              subscribed_background: str, giver_username: str) -> GetSubscriptionSchema:
        return GetSubscriptionSchema(
            tier=subscription.tier,
            date_end=subscription.date_end,
            subscribed_id=subscription.subscribed_id,
            giver_id=subscription.gifted_id,
            total_month=total_month,
            subscribed_username=subscribed_username,
            subscribed_icon=subscribed_icon,
            subscribed_background=subscribed_background,
            giver_username=giver_username,
        )
