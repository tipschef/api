import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.database.service.database import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255), index=True)
    firstname = Column(String(255), index=True)
    lastname = Column(String(255), index=True)
    sub_enabled = Column(Boolean, index=True, default=False)
    is_partner = Column(Boolean, index=True, default=False)
    is_admin = Column(Boolean, index=True, default=False)
    is_cook = Column(Boolean, index=True, default=False)
    is_highlighted = Column(Boolean, index=True, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
