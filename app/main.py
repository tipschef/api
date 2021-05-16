import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.route.home_router import router as home_router
from app.database.service.database_init import init_database
from app.user.route.user_route import router as user_router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors(), 'body': exc.body}),
    )


def setup_router() -> None:
    app.include_router(home_router)
    app.include_router(user_router, prefix='/v1')


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

if __name__ == '__main__':
    configure()
    uvicorn.run(app, host='127.0.0.1', port=5050)
