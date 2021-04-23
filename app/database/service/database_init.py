from app.database.service.database import Base, engine
from app.user.model.user_model import UserModel


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
