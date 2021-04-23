from sqlalchemy import Column, Integer, String

from app.database.service.database import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, index=True)
    password = Column(String(255), index=True)
