import os

import uvicorn
from fastapi import FastAPI

from app.common.route.home_router import router as home_router
from app.database.service.database_init import init_database
from app.user.route.user_route import router as user_router

app = FastAPI()


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


if __name__ == '__main__':
    configure()
    uvicorn.run(app, host='127.0.0.1', port=5050)
