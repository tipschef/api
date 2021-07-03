from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.payment.model.payslip_model import PayslipModel


@dataclass
class PayslipRepository:

    @staticmethod
    def get_all_payslip_from_user_id(database: Session, user_id: int) -> List[PayslipModel]:
        return database.query(PayslipModel).filter(PayslipModel.user_id == user_id).all()

    @staticmethod
    def create_payslip(database: Session, user_id: int, amount: float) -> PayslipModel:
        db_payslip = PayslipModel(user_id=user_id, amount=amount)
        database.add(db_payslip)
        database.commit()
        database.refresh(db_payslip)
        return db_payslip
