import datetime
from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from app.recipe.repository.media.media_repository import MediaRepository
from app.user.exception.user_route_exceptions import CantReachOthersDiscussionException, NotFoundDiscussionException
from app.user.repository.discussion_repository import DiscussionRepository
from app.user.repository.message_repository import MessageRepository
from app.user.repository.user_repository import UserRepository
from app.user.schema.discussion_schema import DiscussionSchema
from app.user.schema.received_message_schema import ReceivedMessageSchema
from app.user.schema.send_message_schema import SendMessageSchema
from app.user.schema.user.user_schema import UserSchema


@dataclass
class DiscussionService:

    @staticmethod
    def add_message_to_discussion(database: Session,
                                  received_message_schema: ReceivedMessageSchema) -> SendMessageSchema:
        discussion = DiscussionRepository.get_discussion_between_people(database, received_message_schema.sender_id,
                                                                        received_message_schema.receiver_id)
        message_model = MessageRepository.create_message(database, received_message_schema.sender_id,
                                                         received_message_schema.content, discussion.id)

        if received_message_schema.sender_id == discussion.first_user_id:
            DiscussionRepository.update_first_user_date(database, discussion.id, message_model.created_date)
        if received_message_schema.sender_id == discussion.second_user_id:
            DiscussionRepository.update_second_user_date(database, discussion.id, message_model.created_date)

        DiscussionRepository.update_last_message_date(database, discussion.id, message_model.created_date)

        return SendMessageSchema.from_received_message(received_message_schema, message_model.created_date)

    @staticmethod
    def get_my_discussions(database: Session, current_user: UserSchema) -> List[DiscussionSchema]:
        discussions = DiscussionRepository.get_user_discussions(database, current_user.id)
        discussion_schemas = []
        for discussion in discussions:
            first_user = UserRepository.get_user_by_id(discussion.first_user_id)
            second_user = UserRepository.get_user_by_id(discussion.second_user_id)

            if first_user.id == current_user.id:
                curr_user = first_user
                interlocutor_user = second_user
            else:
                curr_user = second_user
                interlocutor_user = first_user

            interlocutor_user_profile_media = MediaRepository.get_media_by_id(database, interlocutor_user.profile_media_id)

            interlocutor_user_profile = interlocutor_user_profile_media.path if interlocutor_user_profile_media is not None else None

            discussion_schemas.append(DiscussionSchema.from_model(
                discussion.id,
                curr_user.id,
                interlocutor_user.id,
                interlocutor_user.username,
                interlocutor_user_profile,
                discussion.first_user_date if first_user.id == current_user.id else discussion.second_user_date,
                discussion.last_message_date
            ))
        return discussion_schemas

    @staticmethod
    def create_discussion(database: Session, current_user: UserSchema, interlocutor_username: str):
        interlocutor = UserRepository.get_user_by_username(interlocutor_username)
        discussion = DiscussionRepository.get_discussion_between_people(database, current_user.id, interlocutor.id)
        if discussion is None:
            DiscussionRepository.create_discussion(database, current_user.id, interlocutor.id)

    @staticmethod
    def get_message_by_discussion_id(database: Session, discussion_id: int, current_user: UserSchema) -> List[SendMessageSchema]:
        discussion = DiscussionRepository.get_discussion_by_id(database, discussion_id)
        messages = MessageRepository.get_message_by_discussion_id(database, discussion_id)
        message_schema = []

        if discussion is None:
            raise NotFoundDiscussionException()

        if current_user.id != discussion.first_user_id and current_user.id != discussion.second_user_id:
            raise CantReachOthersDiscussionException()

        if current_user.id == discussion.first_user_id:
            DiscussionRepository.update_first_user_date(database, discussion.id, datetime.datetime.now())
        if current_user.id == discussion.second_user_id:
            DiscussionRepository.update_second_user_date(database, discussion.id, datetime.datetime.now())

        for message in messages:
            receiver_id = discussion.first_user_id if message.id == discussion.second_user_id else discussion.second_user_id
            message_schema.append(SendMessageSchema.from_data(receiver_id, message.sender_id, message.content, message.created_date))
        return message_schema
