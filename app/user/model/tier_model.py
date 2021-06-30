from sqlalchemy import Column, Integer, Float

from app.database.service.database import Base


class TierModel(Base):
    __tablename__ = "tier"

    id = Column(Integer, primary_key=True, index=True)
    tier = Column(Integer, unique=True, index=True)
    price = Column(Float, index=True)
