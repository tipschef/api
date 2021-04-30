from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_db
from app.user.exception.user_route_exceptions import UserAlreadyExistsException
from app.user.schema.user_create_schema import UserCreateSchema
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/users')


@router.get("/")
async def user_route():
    return {"message": "User route"}


@router.post("/", response_model=UserSchema)
async def create_user_route(user: UserCreateSchema, database: Session = Depends(get_db)):
    try:
        created_user_model = UserService.create_user(database=database, user=user)
        return UserSchema.from_user_model(created_user_model)
    except UserAlreadyExistsException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
