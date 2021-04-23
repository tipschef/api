from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime

from app.database.service.database import Base


class SubscriptionModel(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    subscribed_id = Column(Integer, ForeignKey('user.id'), index=True)
    subscriber_id = Column(Integer, ForeignKey('user.id'), index=True)
    gifted_id = Column(Integer, ForeignKey('user.id'), index=True)
    email = Column(String(320), unique=True, index=True)
    tier = Column(Integer, unique=True, index=True)
    is_gifted = Column(Boolean, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
