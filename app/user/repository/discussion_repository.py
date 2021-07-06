from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.user.model.discussion_model import DiscussionModel


@dataclass
class DiscussionRepository:

    @staticmethod
    def get_user_discussions(database: Session, user_id: int) -> List[DiscussionModel]:
        return database.query(DiscussionModel).filter(
            or_(DiscussionModel.first_user_id == user_id, DiscussionModel.second_user_id == user_id)) \
            .all()

    @staticmethod
    def get_discussion_by_id(database: Session, discussion_id: int) -> DiscussionModel:
        return database.query(DiscussionModel).filter(DiscussionModel.id == discussion_id) \
            .first()

    @staticmethod
    def create_discussion(database: Session, user_id: int, interlocutor_id: int) -> DiscussionModel:
        db_discussion = DiscussionModel(first_user_id=user_id, second_user_id=interlocutor_id)
        database.add(db_discussion)
        database.commit()
        database.refresh(db_discussion)
        return db_discussion

    @staticmethod
    def get_discussion_between_people(database: Session, user_id: int, interlocutor_id: int) -> DiscussionModel:
        return database.query(DiscussionModel).filter(
            or_(and_(DiscussionModel.first_user_id == user_id, DiscussionModel.second_user_id == interlocutor_id),
                and_(DiscussionModel.first_user_id == interlocutor_id, DiscussionModel.second_user_id == user_id))) \
            .first()

    @staticmethod
    def update_first_user_date(database: Session, discussion_id: int, date: datetime) -> None:
        database.query(DiscussionModel).filter(DiscussionModel.id == discussion_id).update(
            {DiscussionModel.first_user_date: date})
        database.commit()

    @staticmethod
    def update_second_user_date(database: Session, discussion_id: int, date: datetime) -> None:
        database.query(DiscussionModel).filter(DiscussionModel.id == discussion_id).update(
            {DiscussionModel.second_user_date: date})
        database.commit()

    @staticmethod
    def update_last_message_date(database: Session, discussion_id: int, date: datetime) -> None:
        database.query(DiscussionModel).filter(DiscussionModel.id == discussion_id).update(
            {DiscussionModel.last_message_date: date})
        database.commit()
