import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey

from app.database.service.database import Base


class DiscussionModel(Base):
    __tablename__ = "discussion"

    id = Column(Integer, primary_key=True, index=True)
    first_user_id = Column(Integer, ForeignKey('user.id'), index=True)
    second_user_id = Column(Integer, ForeignKey('user.id'), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    last_message_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    first_user_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    second_user_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
