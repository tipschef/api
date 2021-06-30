from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app.payment.model.payment_model import PaymentModel


@dataclass
class PaymentRepository:

    @staticmethod
    def get_payment_by_user_id(database: Session, user_id: int) -> Optional[PaymentModel]:
        return database.query(PaymentModel).filter(PaymentModel.user_id == user_id).first()

    @staticmethod
    def create_payment(database: Session, user_id: int, account_id: str, customer_id: str) -> PaymentModel:
        db_payment = PaymentModel(user_id=user_id, account_id=account_id, customer_id=customer_id)
        database.add(db_payment)
        database.commit()
        database.refresh(db_payment)
        return db_payment

    @staticmethod
    def update_payment_account_id(database: Session, user_id: int, account_id: str):
        database.query(PaymentModel).filter(PaymentModel.user_id == user_id).update(
            {PaymentModel.account_id: account_id})
        database.commit()

    @staticmethod
    def update_payment_customer_id(database: Session, user_id: int, customer_id: str):
        database.query(PaymentModel).filter(PaymentModel.user_id == user_id).update(
            {PaymentModel.customer_id: customer_id})
        database.commit()
