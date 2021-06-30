from sqlalchemy import Column, Integer, ForeignKey, String

from app.database.service.database import Base


class PaymentModel(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    account_id = Column(String(320), index=True)
    customer_id = Column(String(320), index=True)
