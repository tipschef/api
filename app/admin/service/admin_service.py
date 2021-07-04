from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.admin.exception.admin_service_exceptions import UserNotAdminException
from app.admin.schema.user_admin_schema import UserAdminSchema
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
    def highlight_user_by_id(database: Session, user_to_highlight_id: int, user: UserSchema) -> bool:
        is_admin = UserRepository.get_user_by_id(user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()

        UserRepository.highlight_user_by_id(database, user_to_highlight_id)
        return True

    @staticmethod
    def add_admin_user_by_id(database: Session, user_to_admin_id: int, user: UserSchema) -> bool:
        is_admin = UserRepository.get_user_by_id(user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()

        UserRepository.add_admin_by_user_by_id(database, user_to_admin_id)
        return True

    @staticmethod
    def remove_highlight_user_by_id(database: Session, user_to_partner_id: int, user: UserSchema) -> bool:
        is_admin = UserRepository.get_user_by_id(user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()

        UserRepository.remove_highlight_user_by_id(database, user_to_partner_id)
        return True

    @staticmethod
    def get_users(database: Session, current_user: UserSchema) -> List[UserAdminSchema]:
        is_admin = UserRepository.get_user_by_id(current_user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()
        user_admin_schema_list = []
        users = UserRepository.get_all_users(database)

        for user in users:
            bank_information_is_filled = PaymentRepository.get_payment_by_user_id(database, user.id).account_id != ''

            user_admin_schema_list.append(UserAdminSchema.from_model(user, bank_information_is_filled))

        return user_admin_schema_list
