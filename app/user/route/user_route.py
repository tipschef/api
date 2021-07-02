from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database.service.database_instance import get_database
from app.payment.exception.payment_service_exceptions import NoPaymentMethodException
from app.recipe.schema.media.media_schema import MediaSchema
from app.recipe.schema.recipe.recipe_response_extended_schema import RecipeResponseExtendedSchema
from app.recipe.service.recipe_service import RecipeService
from app.user.exception.subscription_service_exceptions import UserNotPartnerException, AlreadySubscribedToUser, \
    TierDoesNotExist, NotEnoughFollowersException, UserNotSubscribedException
from app.user.exception.user_route_exceptions import UserAlreadyExistsException, UsernameAlreadyExistsException, \
    UsernameNotFoundException, WrongUploadFileType, UserIdNotFoundException, UsernameNotFound, \
    EmailAlreadyExistsException
from app.user.schema.create_random_subscription_schema import CreateRandomSubscriptionSchema
from app.user.schema.create_subscription_schema import CreateSubscriptionSchema
from app.user.schema.dashboard_schema import DashboardSchema
from app.user.schema.get_subscription_schema import GetSubscriptionSchema
from app.user.schema.tier_schema import TierSchema
from app.user.schema.user.user_auth_schema import UserAuthSchema
from app.user.schema.user.user_create_schema import UserCreateSchema
from app.user.schema.user.user_detailed_schema import UserDetailedSchema
from app.user.schema.user.user_schema import UserSchema
from app.user.schema.user.user_shortened_schema import UserShortenedSchema
from app.user.schema.user.user_update_schema import UserUpdateSchema
from app.user.service.dashboard_service import DashboardService
from app.user.service.follow_service import FollowService
from app.user.service.subscription_service import SubscriptionService
from app.user.service.user_service import UserService

router = APIRouter(prefix='/users')


@router.get('/', tags=['users'])
async def user_route():
    return {'message': 'User route'}


@router.post('/', response_model=UserSchema, tags=['users'])
async def create_user_route(user: UserCreateSchema, database: Session = Depends(get_database)):
    try:
        created_user_model = UserService.create_user(database=database, user=user)
        return UserSchema.from_user_model(created_user_model)
    except UserAlreadyExistsException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except UsernameAlreadyExistsException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/id/{user_id}', response_model=UserDetailedSchema, tags=['users'])
async def get_user_by_user_id(user_id: int, database: Session = Depends(get_database)) -> UserDetailedSchema:
    try:
        return UserService.get_user_by_user_id(database, user_id)
    except UserIdNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/me', response_model=UserDetailedSchema, tags=['users'])
async def get_user_information(database: Session = Depends(get_database),
                               current_user: UserSchema = Depends(
                                   UserService.get_current_active_user)) -> UserDetailedSchema:
    try:
        return UserService.get_my_informations(database, current_user)
    except UsernameNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/search', response_model=List[UserDetailedSchema], tags=['users'])
async def search_user(username: str, database: Session = Depends(get_database),
                      current_user: UserSchema = Depends(UserService.get_current_active_user)) \
        -> List[UserDetailedSchema]:
    try:
        return UserService.search_username(database, username, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/subscribe/tier', response_model=List[TierSchema], tags=['subscribe'])
async def get_tiers(database: Session = Depends(get_database)) -> List[TierSchema]:
    try:
        return UserService.get_tiers(database)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/subscribe', response_model=dict, tags=['users', 'subscribe'])
async def subscribe_by_username(create_subscription: CreateSubscriptionSchema,
                                database: Session = Depends(get_database),
                                current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        SubscriptionService.subscribe_to_someone_by_username(database, current_user, create_subscription)
        return {'Status': 'Done'}
    except UserNotPartnerException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except UsernameNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except AlreadySubscribedToUser as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except NoPaymentMethodException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except TierDoesNotExist as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/subscribe/on_going', response_model=List[GetSubscriptionSchema], tags=['subscribe'])
async def get_ongoing_subscriptions(database: Session = Depends(get_database), current_user: UserSchema = Depends(
    UserService.get_current_active_user)) -> List[GetSubscriptionSchema]:
    try:
        return SubscriptionService.get_ongoing_subscriptions(database, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/subscribe/gifted', response_model=List[GetSubscriptionSchema], tags=['subscribe'])
async def get_gifted_subscriptions(database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[GetSubscriptionSchema]:
    try:
        return SubscriptionService.get_gifted_subscriptions(database, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/subscribe/expired', response_model=List[GetSubscriptionSchema], tags=['subscribe'])
async def get_expired_subscriptions(database: Session = Depends(get_database), current_user: UserSchema = Depends(UserService.get_current_active_user)) -> List[GetSubscriptionSchema]:
    try:
        return SubscriptionService.get_expired_subscriptions(database, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/subscribe/available/{username}', response_model=dict, tags=['subscribe'])
async def count_user_available_followers(username: str,
                                         database: Session = Depends(get_database)) -> dict:
    try:
        return {'available_followers': SubscriptionService.count_user_available_followers(database, username)}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.post('/subscribe/gift', response_model=dict, tags=['users', 'subscribe'])
async def gift_a_subscription_by_username(create_random_subscription: CreateRandomSubscriptionSchema,
                                          database: Session = Depends(get_database),
                                          current_user: UserSchema = Depends(
                                              UserService.get_current_active_user)) -> dict:
    try:
        SubscriptionService.gist_random_subscription(database, current_user, create_random_subscription)
        return {'Status': 'Done'}
    except UserNotPartnerException as exception:
        raise HTTPException(status_code=403, detail=str(exception))
    except UsernameNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except AlreadySubscribedToUser as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except NoPaymentMethodException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except TierDoesNotExist as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except UserNotSubscribedException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except NotEnoughFollowersException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/follow', response_model=dict, tags=['users', 'follow'])
async def follow_user_by_username(username: str, database: Session = Depends(get_database),
                                  current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:
        if FollowService.follow_someone_by_username(database, current_user, username):
            return {'Status': 'Done'}
        return {'Status': 'Already following'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/unfollow', response_model=dict, tags=['users', 'follow'])
async def unfollow_user_by_username(username: str, database: Session = Depends(get_database),
                                    current_user: UserSchema = Depends(UserService.get_current_active_user)) -> dict:
    try:

        if FollowService.unfollow_someone_by_username(database, current_user, username):
            return {'Status': 'Done'}
        return {'Status': 'You were not following'}
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/update/profile', response_model=MediaSchema, tags=['users', 'profile', 'media'])
async def upload_profile_picture(file: UploadFile = File(...),
                                 database: Session = Depends(get_database),
                                 current_user: UserAuthSchema = Depends(
                                     UserService.get_current_active_user)) -> MediaSchema:
    try:
        media = UserService.update_user_profile_picture(database, current_user.id, file)
        return media
    except WrongUploadFileType as exception:
        raise HTTPException(status_code=415, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/update/background', response_model=MediaSchema, tags=['users', 'profile', 'media'])
async def upload_background_picture(file: UploadFile = File(...),
                                    database: Session = Depends(get_database),
                                    current_user: UserAuthSchema = Depends(
                                        UserService.get_current_active_user)) -> MediaSchema:
    try:
        media = UserService.update_user_background_picture(database, current_user.id, file)
        return media
    except WrongUploadFileType as exception:
        raise HTTPException(status_code=415, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.patch('/update/data', response_model=dict, tags=['users', 'profile', 'media'])
async def update_profile(user_data: UserUpdateSchema, database: Session = Depends(get_database),
                         current_user: UserAuthSchema = Depends(
                             UserService.get_current_active_user)) -> dict:
    try:
        if UserService.update_user_profile(user_data, database, current_user):
            return {'status': 'updated'}

    except UsernameAlreadyExistsException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except EmailAlreadyExistsException as exception:
        raise HTTPException(status_code=400, detail=str(exception))
    except WrongUploadFileType as exception:
        raise HTTPException(status_code=415, detail=str(exception))


@router.get('/dashboard/data', response_model=List[DashboardSchema], tags=['users', 'dashboard'])
async def get_dashboard_data(database: Session = Depends(get_database),
                             current_user: UserAuthSchema = Depends(
                                 UserService.get_current_active_user)) -> List[DashboardSchema]:
    try:
        return DashboardService.get_dashboard_data(database, current_user)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}/recipes', response_model=List[RecipeResponseExtendedSchema], tags=['users', 'recipes'])
async def get_recipes_from_username(username: str, per_page: int = 20, page: int = 1,
                                    database: Session = Depends(get_database),
                                    current_user: UserSchema = Depends(UserService.get_current_active_user)) \
        -> List[RecipeResponseExtendedSchema]:
    try:
        return RecipeService.get_all_recipe_for_specific_user(database, current_user, username, per_page, page)
    except UsernameNotFound as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/highlight', response_model=List[UserShortenedSchema], tags=['users'])
async def get_highlights(database: Session = Depends(get_database),
                         _: UserSchema = Depends(UserService.get_current_active_user)) \
        -> List[UserShortenedSchema]:
    try:
        return UserService.get_highlighted(database)
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')


@router.get('/{username}', response_model=UserDetailedSchema, tags=['users'])
async def get_user_by_username(username: str, database: Session = Depends(get_database),
                               current_user: UserSchema = Depends(
                                   UserService.get_current_active_user)) -> UserDetailedSchema:
    try:
        return UserService.get_user_by_username(database, username, current_user)
    except UsernameNotFoundException as exception:
        raise HTTPException(status_code=404, detail=str(exception))
    except Exception as exception:
        print(exception)
        raise HTTPException(status_code=500, detail='Server exception')
