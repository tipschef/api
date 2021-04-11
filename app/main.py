import os

import uvicorn
from fastapi import FastAPI

from app.common.service.secret_manager_service import SecretManagerService
from app.common.route.home_router import router as home_router
from app.database.service.database import Base, engine
from app.database.service.database_init import init_database
from app.user.route.user_route import router as user_router

app = FastAPI()


def setup_router() -> None:
    app.include_router(home_router)
    app.include_router(user_router, prefix='/v1')


def setup_database() -> None:
    init_database()


def configure() -> None:
    project_id = os.getenv('PROJECT_ID')
    env = os.getenv('PROJECT_ENV')
    setup_database()
    setup_router()
    secret_manager_service = SecretManagerService(project_id, 'secret-api', env)


configure()
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5050)
