import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

from app.authentication.route.authentication_route import router as authentication_router
from app.book.route.book_route import router as book_router
from app.common.route.home_router import router as home_router
from app.database.service.database_init import init_database
from app.payment.route.payment_route import router as payment_router
from app.recipe.route.media_category_route import router as media_category_route
from app.recipe.route.recipe_category_route import router as recipe_category_route
from app.recipe.route.recipe_cooking_type_route import router as recipe_cooking_type_route
from app.recipe.route.recipe_route import router as recipe_route
from app.user.route.user_route import router as user_router
from app.admin.route.admin_route import router as admin_router
from app.user.service.dashboard_service import DashboardService

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors(), 'body': exc.body}),
    )


@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
def get_partner_data() -> None:
    DashboardService.create_dashboard_data()


def setup_router() -> None:
    app.include_router(home_router)
    app.include_router(user_router, prefix='/v1')
    app.include_router(authentication_router, prefix='/v1')
    app.include_router(recipe_route, prefix='/v1')
    app.include_router(media_category_route, prefix='/v1')
    app.include_router(recipe_category_route, prefix='/v1')
    app.include_router(recipe_cooking_type_route, prefix='/v1')
    app.include_router(book_router, prefix='/v1')
    app.include_router(payment_router, prefix='/v1')
    app.include_router(admin_router, prefix='/v1')


def setup_database() -> None:
    init_database()


def check_env_variable() -> None:
    # TODO : CHECK ENV VARIABLE
    pass


def configure() -> None:
    check_env_variable()
    setup_database()
    setup_router()


configure()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5050)
