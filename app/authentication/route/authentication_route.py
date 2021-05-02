from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.authentication.exception.authentication_service_exceptions import WrongCredentialException
from app.authentication.schema.authenticated_schema import Token, AuthenticatedSchema
from app.authentication.schema.authentication_schema import AuthenticationSchema
from app.authentication.service.authentication_service import AuthenticationService
from app.database.service.database_instance import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth')


@router.post('/token', response_model=Token)
async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db)):
    try:
        user = AuthenticationSchema(username=form_data.username, password=form_data.password)
        reponse = AuthenticationService.authentifie_user(database, user)
        return {"access_token": reponse.token, "token_type": reponse.token_type}
    except WrongCredentialException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/', response_model=Any)
async def authenticate_user(current_user: AuthenticationSchema = Depends(AuthenticationService.get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

