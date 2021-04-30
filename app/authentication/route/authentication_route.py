from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.authentication.exception.authentication_service_exceptions import WrongCredentialException
from app.authentication.schema.authenticated_schema import AuthenticatedSchema
from app.authentication.schema.authentication_schema import AuthenticationSchema
from app.authentication.service.authentication_service import AuthenticationService
from app.database.service.database_instance import get_db

router = APIRouter(prefix='/auth')


@router.post('/', response_model=AuthenticatedSchema)
async def authenticate_user(authentication_user: AuthenticationSchema,  database: Session = Depends(get_db)):
    try:
        return AuthenticationService.authentifie_user(database, authentication_user)
    except WrongCredentialException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
