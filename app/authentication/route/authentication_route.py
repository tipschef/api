from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.authentication.exception.authentication_service_exceptions import WrongCredentialException
from app.authentication.schema.authenticated_schema import Token
from app.authentication.schema.authentication_schema import AuthenticationSchema
from app.authentication.service.authentication_service import AuthenticationService
from app.user.schema.user_schema import UserSchema
from app.user.service.user_service import UserService

router = APIRouter(prefix='/auth')


@router.post('/token', response_model=Token, tags=['authentication'])
async def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = AuthenticationSchema(username=form_data.username, password=form_data.password)
        reponse = AuthenticationService.authentifie_user(user)
        return {"access_token": reponse.token, "token_type": reponse.token_type}
    except WrongCredentialException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/', response_model=dict, tags=['authentication'])
async def get_user_data(current_user: UserSchema = Depends(UserService.get_current_active_user)):
    return current_user.dict()
