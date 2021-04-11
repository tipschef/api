from sqlalchemy.orm import Session

from app.user.model.user_model import User
from app.user.schema.user_create_schema import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + 'notreallyhashed'
    db_user = User(email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
