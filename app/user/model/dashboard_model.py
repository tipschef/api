import datetime

from sqlalchemy import Column, DateTime, Integer

from app.database.service.database import Base


class DashboardModel(Base):
    __tablename__ = 'dashboard'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    follower = Column(Integer, index=True)
    sub = Column(Integer, index=True)
    like = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
