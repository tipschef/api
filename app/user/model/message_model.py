import datetime

from sqlalchemy import Column, DateTime, Integer, ForeignKey, String

from app.database.service.database import Base


class MessageModel(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('user.id'), index=True)
    discussion_id = Column(Integer, ForeignKey('discussion.id'), index=True)
    content = Column(String(255), index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    media = Column(String(500), index=True)
