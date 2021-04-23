from sqlalchemy import Column, DateTime, Integer, ForeignKey
import datetime

from app.database.service.database import Base


class FollowModel(Base):
    __tablename__ = "follow"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('user.id'), index=True)
    followed_id = Column(Integer, ForeignKey('user.id'), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    stop_date = Column(DateTime, index=True)
