from fastapi import APIRouter, Depends, HTTPException

from app.database.service.database_instance import get_db
from app.user.schema.user_create_schema import UserCreate
from app.user.schema.user_schema import User
from sqlalchemy.orm import Session

from app.user.service.user_service import get_user_by_email, create_user

router = APIRouter(prefix='/users')


@router.get("/")
async def user_route():
    return {"message": "User route"}


@router.post("/", response_model=User)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)
