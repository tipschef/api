from __future__ import annotations

from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import SecretStr

from app.authentication.exception.authentication_service_exceptions import WrongCredentialException
from app.authentication.schema.authenticated_schema import AuthenticatedSchema
from app.authentication.schema.authentication_schema import AuthenticationSchema
from app.user.model.user_model import UserModel
from app.user.repository.user_repository import UserRepository
from app.user.schema.user_schema import UserSchema

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = 'HS256'
SECRET_KEY = 'dsfljldfgjlksdfgjlksdfjglikfdg'

PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/token')


class AuthenticationService:

    @staticmethod
    def get_user(username: str) -> Optional[UserModel]:
        return UserRepository.get_user_by_username(username)

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
        return PWD_CONTEXT.verify(plain_password.get_secret_value(), hashed_password)

    @staticmethod
    def authentifie_user(user: AuthenticationSchema) -> AuthenticatedSchema:
        user_already_exist = AuthenticationService.get_user(user.username)
        if not user_already_exist:
            raise WrongCredentialException
        if not AuthenticationService._verify_password(user.password, user_already_exist.password):
            raise WrongCredentialException

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        acces_token = AuthenticationService._create_access_token(data={'sub': user.username},
                                                                 expires_delta=access_token_expires)
        return AuthenticatedSchema(username=user.username, token=acces_token, token_type='Bearer')

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get('sub')
            if username is None:
                raise Exception
        except JWTError:
            raise Exception
        user = UserSchema.from_user_model(AuthenticationService.get_user(username))
        if user is None:
            raise Exception
        return user
