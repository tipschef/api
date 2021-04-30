from app.database.service.database import Base, engine


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
