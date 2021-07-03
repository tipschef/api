import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime

from app.database.service.database import Base


class PayslipModel(Base):
    __tablename__ = "payslip"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    amount = Column(Float, index=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
