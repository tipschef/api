from dataclasses import dataclass
from typing import List

import stripe
from fastapi import UploadFile
from sqlalchemy.orm import Session
from stripe import Account, Token, Customer, File

from app.admin.exception.admin_service_exceptions import UserNotAdminException
from app.book.repository.book_purchase_repository import BookPurchaseRepository
from app.common.service.secret_manager_service import get_secret_manager_service
from app.payment.exception.payment_service_exceptions import NoAccountIdException, NoPaymentMethodException
from app.payment.repository.payment_repository import PaymentRepository
from app.payment.repository.payslip_repository import PayslipRepository
from app.payment.schema.bank_account_schema import BankAccountSchema
from app.payment.schema.card_schema import CardSchema
from app.payment.schema.customer_schema import CustomerSchema
from app.payment.schema.payment_intent_schema import PaymentIntentSchema
from app.payment.schema.payment_schema import PaymentSchema
from app.payment.schema.payslip_schema import PayslipSchema
from app.user.repository.subscription_repository import SubscriptionRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.user.user_schema import UserSchema

PART_SUB = 0.4
PART_BOOK = 0.6


@dataclass
class PaymentService:

    def __post_init__(self):
        self.init_data()

    @staticmethod
    def init_data():
        secret_manager_service = get_secret_manager_service()
        secret_content = secret_manager_service.get_secret_json()
        stripe.api_key = secret_content.get('stripe_api_key')

    @staticmethod
    def create_bank_account(database: Session, user: UserSchema, bank_account: BankAccountSchema) -> Account:
        payment = PaymentRepository.get_payment_by_user_id(database, user.id)
        if payment is None:
            raise NoAccountIdException()
        account = PaymentService._get_bank_account(payment.account_id)
        token = stripe.Token.create(
            bank_account={
                'country': account.individual.address.country,
                'currency': account.default_currency,
                'account_holder_name': f'{account.individual.first_name} {account.individual.last_name}',
                'account_holder_type': account.business_type,
                'account_number': bank_account.iban,
            }
        )
        stripe.Account.create_external_account(
            payment.account_id,
            external_account=token.id,
        )
        return PaymentService._get_bank_account(payment.account_id)

    @staticmethod
    def _get_bank_account(account_id: str) -> Account:
        return stripe.Account.retrieve(account_id)

    @staticmethod
    def get_account_by_id(database: Session, user: UserSchema) -> Account:
        payment = PaymentRepository.get_payment_by_user_id(database, user.id)
        if payment is None or payment.account_id == '':
            raise NoAccountIdException()
        return PaymentService._get_bank_account(payment.account_id)

    @staticmethod
    def _create_stripe_token(payment_schema: PaymentSchema) -> Token:
        birthdate = payment_schema.birthdate.split('-')
        return stripe.Token.create(account={

            'business_type': 'individual',
            'individual': {
                'first_name': payment_schema.first_name,
                'last_name': payment_schema.last_name,
                'email': payment_schema.email,
                'address': {
                    'city': payment_schema.address_city,
                    'country': payment_schema.address_country,
                    'postal_code': payment_schema.address_postal_code,
                    'line1': payment_schema.address_line1,
                },
                'dob': {
                    'day': birthdate[2],
                    'month': birthdate[1],
                    'year': birthdate[0],
                },
                'gender': payment_schema.gender,
                'phone': payment_schema.phone,
                'verification': {
                    'document': {
                        'back': payment_schema.id_verso,
                        'front': payment_schema.id_recto,
                    },
                    'additional_document': {
                        'back': payment_schema.id_verso,
                        'front': payment_schema.id_recto,
                    },
                },
            },
            'tos_shown_and_accepted': True,
        })

    @staticmethod
    def create_account(database: Session, payment_schema: PaymentSchema, user: UserSchema) -> Account:
        token = PaymentService._create_stripe_token(payment_schema)

        account = stripe.Account.create(type='custom',
                                        capabilities={
                                            'card_payments': {'requested': True},
                                            'transfers': {'requested': True},
                                        },
                                        business_profile={
                                            'support_url': 'www.google.com',
                                            'url': 'www.google.com',
                                            'mcc': '6513',
                                        },
                                        account_token=token.id
                                        )
        payment = PaymentRepository.get_payment_by_user_id(database, user.id)
        if payment is None:
            PaymentRepository.create_payment(database, user.id, account.stripe_id, '')
        elif payment.account_id == '':
            PaymentRepository.update_payment_account_id(database, user.id, account.stripe_id)

        return account

    @staticmethod
    def create_customer(customer: CustomerSchema) -> Customer:
        return stripe.Customer.create(email=customer.email, name=customer.name, phone=customer.phone)

    @staticmethod
    def get_customer_by_id(customer_id: str) -> Customer:
        return stripe.Customer.retrieve(customer_id)

    @staticmethod
    def create_payment_intent(database: Session, user: UserSchema, payment_intent: PaymentIntentSchema) -> None:
        customer = PaymentService.get_or_create_customer(database, user)
        payment = PaymentRepository.get_payment_by_user_id(database, user.id)
        if customer.invoice_settings.default_payment_method is None:
            raise NoPaymentMethodException()
        try:
            stripe.PaymentIntent.create(
                amount=payment_intent.amount,
                currency='eur',
                customer=payment.customer_id,
                payment_method_types=['card'],
                payment_method=customer.invoice_settings.default_payment_method,
                confirm=True
            )
        except Exception:
            raise Exception()

    @staticmethod
    def get_or_create_customer(database: Session, user: UserSchema):
        payment = PaymentRepository.get_payment_by_user_id(database, user.id)
        if payment is None:
            user_db = UserRepository.get_user_by_id(user.id)
            customer = PaymentService.create_customer(
                CustomerSchema(email=user_db.email, name=f'{user_db.firstname} {user_db.lastname}',
                               phone=user_db.phone))
            PaymentRepository.create_payment(database, user.id, '', customer.stripe_id)
        elif payment.customer_id == '':
            user_db = UserRepository.get_user_by_id(user.id)
            customer = PaymentService.create_customer(
                CustomerSchema(email=user_db.email, name=f'{user_db.firstname} {user_db.lastname}',
                               phone=user_db.phone))
            PaymentRepository.update_payment_customer_id(database, user.id, customer.stripe_id)

        payment = PaymentRepository.get_payment_by_user_id(database, user.id)
        return PaymentService.get_customer_by_id(payment.customer_id)

    @staticmethod
    def create_payment_method(database: Session, user: UserSchema, card: CardSchema):
        customer = PaymentService.get_or_create_customer(database, user)
        payment_methode = stripe.PaymentMethod.create(
            type='card',
            card={
                'number': card.number,
                'exp_month': card.exp_month,
                'exp_year': card.exp_year,
                'cvc': card.cvc,
            })

        stripe.PaymentMethod.attach(
            payment_methode.stripe_id,
            customer=customer.stripe_id,
        )

        stripe.Customer.modify(customer.stripe_id,
                               invoice_settings={'default_payment_method': payment_methode.stripe_id})

    @staticmethod
    def upload_id(media: UploadFile) -> File:
        return stripe.File.create(purpose='identity_document', file=media.file)

    @staticmethod
    def get_payment_method_information(database: Session, user: UserSchema) -> int:
        customer = PaymentService.get_or_create_customer(database, user)
        payment_method = customer.invoice_settings.default_payment_method
        if payment_method is None:
            raise NoPaymentMethodException
        return stripe.PaymentMethod.retrieve(payment_method).card.last4

    @staticmethod
    def delete_payment_method(database: Session, user: UserSchema) -> None:
        customer = PaymentService.get_or_create_customer(database, user)
        payment_method = customer.invoice_settings.default_payment_method
        if payment_method is None:
            raise NoPaymentMethodException
        stripe.PaymentMethod.detach(payment_method)

    @staticmethod
    def delete_account(database: Session, user: UserSchema) -> dict:
        payment = PaymentRepository.get_payment_by_user_id(database, user.id)
        if payment is None or payment.account_id == '':
            raise NoAccountIdException()
        response = stripe.Account.delete(payment.account_id)
        PaymentRepository.update_payment_account_id(database, user.id, '')

        return response

    @staticmethod
    def pay_every_partner(database: Session, user: UserSchema):
        is_admin = UserRepository.get_user_by_id(user.id).is_admin
        if not is_admin:
            raise UserNotAdminException()
        partners_to_pay = UserRepository.get_partners(database)
        for partner_to_pay in partners_to_pay:
            PaymentService._transfer_to_account(database, partner_to_pay.id)

    @staticmethod
    def _transfer_to_account(database: Session, user_to_pay_id: int):
        payment = PaymentRepository.get_payment_by_user_id(database, user_to_pay_id)
        if payment is None or payment.account_id == '':
            raise NoAccountIdException()

        subs = SubscriptionRepository.get_all_subscription_for_a_partner(database, user_to_pay_id)
        total_cost_subs = sum([sub[1].price for sub in subs]) * PART_SUB

        books = BookPurchaseRepository.get_purchase_by_book_id(database, user_to_pay_id)
        total_cost_books = sum([book[1].price_euro for book in books]) * PART_BOOK
        total = round((total_cost_subs + total_cost_books) * 100)
        stripe.Transfer.create(amount=total,
                               currency="eur",
                               destination=payment.account_id)

        PayslipRepository.create_payslip(database, user_to_pay_id, total)

    @staticmethod
    def get_my_payslips(database: Session, user: UserSchema) -> List[PayslipSchema]:
        payslips = PayslipRepository.get_all_payslip_from_user_id(database, user.id)
        return [PayslipSchema(user_id=x.user_id, amount=x.amount, created_date=x.created_date) for x in payslips]

    @staticmethod
    def has_payment_method(database: Session, user: UserSchema) -> bool:
        customer = PaymentService.get_or_create_customer(database, user)
        return customer.invoice_settings.default_payment_method is not None


def get_payment_service() -> PaymentService:
    return PaymentService()
