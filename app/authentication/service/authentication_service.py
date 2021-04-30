from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.authentication.exception.authentication_service_exceptions import WrongCredentialException
from app.authentication.schema.authenticated_schema import AuthenticatedSchema
from app.authentication.schema.authentication_schema import AuthenticationSchema
from app.user.model.user_model import UserModel
from app.user.repository.user_repository import UserRepository

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'
SECRET_KEY = 'dsfljldfgjlksdfgjlksdfjglikfdg'

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:

    @staticmethod
    def _does_user_exists(database: Session, user: AuthenticationSchema) -> Optional[UserModel]:
        return UserRepository.get_user_by_email(database, user.email)

    @staticmethod
    def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def _verify_password(plain_password: SecretStr, hashed_password: str):
        print(plain_password.get_secret_value())
        print(hashed_password)
        return PWD_CONTEXT.verify(plain_password.get_secret_value(), hashed_password)

    @staticmethod
    def authentifie_user(database: Session, user: AuthenticationSchema) -> AuthenticatedSchema:
        user_already_exist = AuthenticationService._does_user_exists(database, user)
        if not user_already_exist:
            raise WrongCredentialException
        if not AuthenticationService._verify_password(user.password, user_already_exist.password):
            raise WrongCredentialException

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        acces_token = AuthenticationService._create_access_token(data={'sub': user.email},
                                                                 expires_delta=access_token_expires)
        return AuthenticatedSchema(email=user.email, token=acces_token)
