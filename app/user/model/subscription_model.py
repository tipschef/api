import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey

from app.database.service.database import Base


class SubscriptionModel(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    subscribed_id = Column(Integer, ForeignKey('user.id'), index=True)
    subscriber_id = Column(Integer, ForeignKey('user.id'), index=True)
    gifted_id = Column(Integer, ForeignKey('user.id'), index=True)
    tier = Column(Integer, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    date_end = Column(DateTime, index=True)
