from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.admin.exception.admin_service_exceptions import UserNotAdminException
from app.payment.exception.payment_service_exceptions import NoAccountIdException
from app.payment.repository.payment_repository import PaymentRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.user.user_schema import UserSchema


@dataclass
class AdminService:

    @staticmethod
    def set_user_to_partner(database: Session, user_to_partner_id: int, user: UserSchema) -> bool:
        is_admin = UserRepository.get_user_by_id(user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()
        payment_data = PaymentRepository.get_payment_by_user_id(database, user_to_partner_id)
        if payment_data.account_id == '':
            raise NoAccountIdException()

        UserRepository.set_user_to_partner(database, user_to_partner_id)
        return True

    @staticmethod
    def remove_user_partner(database: Session, user_to_partner_id: int, user: UserSchema) -> bool:
        is_admin = UserRepository.get_user_by_id(user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()

        UserRepository.remove_user_partner(database, user_to_partner_id)
        return True

    @staticmethod
    def highlight_user_by_id(database: Session, user_to_partner_id: int, user: UserSchema) -> bool:
        is_admin = UserRepository.get_user_by_id(user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()

        UserRepository.highlight_user_by_id(database, user_to_partner_id)
        return True

    @staticmethod
    def remove_highlight_user_by_id(database: Session, user_to_partner_id: int, user: UserSchema) -> bool:
        is_admin = UserRepository.get_user_by_id(user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()

        UserRepository.remove_highlight_user_by_id(database, user_to_partner_id)
        return True
