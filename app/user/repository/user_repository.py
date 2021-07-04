from dataclasses import dataclass
from typing import Optional, List, Tuple

from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.recipe.model.media.media_model import MediaModel
from app.user.model.user_model import UserModel
from app.user.schema.user.user_create_schema import UserCreateSchema
from app.user.schema.user.user_schema import UserSchema
from app.user.schema.user.user_update_schema import UserUpdateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class UserRepository:

    @staticmethod
    def get_user_by_email(database: Session, email: str) -> Optional[UserModel]:
        return database.query(UserModel).filter(UserModel.email == email).first()

    @staticmethod
    def get_partners(database: Session) -> List[UserModel]:
        return database.query(UserModel).filter(UserModel.is_partner.is_(True)).all()

    @staticmethod
    def get_all_users(database: Session) -> List[UserModel]:
        return database.query(UserModel).all()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[UserModel]:
        for database in get_database():
            return database.query(UserModel).filter(UserModel.username == username).first()

    @staticmethod
    def search_username(database: Session, username: str) -> List[UserModel]:
        return database.query(UserModel).filter(UserModel.username.contains(username)).all()

    @staticmethod
    def get_highlighted(database: Session) -> List[Tuple[UserModel, MediaModel]]:
        return database.query(UserModel, MediaModel).join(MediaModel,
                                                          MediaModel.id == UserModel.profile_media_id).filter(
            UserModel.is_highlighted.is_(True)).all()

    @staticmethod
    def create_user(database: Session, user: UserCreateSchema) -> UserModel:
        hashed_password = user.password.get_secret_value()
        db_user = UserModel(email=user.email, password=pwd_context.hash(hashed_password), username=user.username)
        database.add(db_user)
        database.commit()
        database.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[UserModel]:
        for database in get_database():
            return database.query(UserModel).filter(UserModel.id == user_id).first()

    @staticmethod
    def update_profile_picture(database: Session, user_id: int, profile_media_id: int) -> None:
        database.query(UserModel).filter(UserModel.id == user_id).update(
            {UserModel.profile_media_id: profile_media_id})
        database.commit()

    @staticmethod
    def update_background_picture(database: Session, user_id: int, background_media_id: int) -> None:
        database.query(UserModel).filter(UserModel.id == user_id).update(
            {UserModel.background_media_id: background_media_id})
        database.commit()

    @staticmethod
    def update_user_information_with_password(user_data: UserUpdateSchema, database: Session,
                                              user_to_update: UserSchema) -> None:
        try:
            database.query(UserModel).filter(UserModel.id == user_to_update.id).update(
                {UserModel.username: user_data.username,
                 UserModel.email: user_data.email,
                 UserModel.firstname: user_data.firstname,
                 UserModel.lastname: user_data.lastname,
                 UserModel.password: pwd_context.hash(user_data.password.get_secret_value()),
                 UserModel.description: user_data.description}
            )
            database.commit()
        except IntegrityError:
            print('existe déja')

        except Exception as exception:
            print(exception)

    @staticmethod
    def update_user_information_without_password(user_data: UserUpdateSchema, database: Session,
                                                 user_to_update: UserSchema) -> None:
        try:
            database.query(UserModel).filter(UserModel.id == user_to_update.id).update(
                {UserModel.username: user_data.username,
                 UserModel.email: user_data.email,
                 UserModel.firstname: user_data.firstname,
                 UserModel.lastname: user_data.lastname,
                 UserModel.description: user_data.description}
            )
            database.commit()
        except IntegrityError:
            print('existe déja')

        except Exception as exception:
            print(exception)

    @staticmethod
    def set_user_to_partner(database: Session, user_id: int) -> None:
        database.query(UserModel).filter(UserModel.id == user_id).update(
            {UserModel.is_partner: True}
        )
        database.commit()

    @staticmethod
    def remove_user_partner(database: Session, user_id: int) -> None:
        database.query(UserModel).filter(UserModel.id == user_id).update(
            {UserModel.is_partner: False}
        )
        database.commit()

    @staticmethod
    def highlight_user_by_id(database: Session, user_id: int) -> None:
        database.query(UserModel).filter(UserModel.id == user_id).update(
            {UserModel.is_highlighted: True}
        )
        database.commit()

    @staticmethod
    def add_admin_by_user_by_id(database: Session, user_id: int) -> None:
        database.query(UserModel).filter(UserModel.id == user_id).update(
            {UserModel.is_admin: True}
        )
        database.commit()

    @staticmethod
    def remove_highlight_user_by_id(database: Session, user_id: int) -> None:
        database.query(UserModel).filter(UserModel.id == user_id).update(
            {UserModel.is_highlighted: False}
        )
        database.commit()
