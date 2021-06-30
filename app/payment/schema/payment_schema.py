from pydantic import BaseModel
from stripe import Account


class PaymentSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    address_city: str
    address_country: str
    address_postal_code: str
    address_line1: str
    birthdate: str
    gender: str
    phone: str
    id_recto: str
    id_verso: str

    @staticmethod
    def from_account(account: Account):
        data = account.individual
        return PaymentSchema(first_name=data.first_name,
                             last_name=data.last_name,
                             email=data.email,
                             address_city=data.address.city,
                             address_country=data.address.country,
                             address_postal_code=data.address.postal_code,
                             address_line1=data.address.line1,
                             birthdate=f'{data.dob.year}-{data.dob.month}-{data.dob.day}',
                             gender=data.gender,
                             phone=data.phone, id_recto=data.verification.document.front,
                             id_verso=data.verification.document.back)
