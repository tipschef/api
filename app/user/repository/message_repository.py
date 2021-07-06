from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.user.model.message_model import MessageModel


@dataclass
class MessageRepository:

    @staticmethod
    def get_message_by_discussion_id(database: Session, discussion_id: int) -> List[MessageModel]:
        return database.query(MessageModel).filter(MessageModel.discussion_id == discussion_id) \
            .all()

    @staticmethod
    def create_message(database: Session, user_id: int, content: str, discussion_id: int) -> MessageModel:
        db_message = MessageModel(sender_id=user_id, content=content, discussion_id=discussion_id)
        database.add(db_message)
        database.commit()
        database.refresh(db_message)
        return db_message
