import os

import uvicorn
from fastapi import FastAPI

from app.helpers.secret_manager_engine import SecretManagerEngine
from router.home_router import router as home_router
from router.user_router import router as user_router

app = FastAPI()


def setup_router() -> None:
    app.include_router(home_router)
    app.include_router(user_router, prefix='/v1')


def configure() -> None:
    project_id = os.getenv('PROJECT_ID')
    env = os.getenv('PROJECT_ENV')
    setup_router()
    secret_manager_engine = SecretManagerEngine(project_id, 'secret-api', env)


configure()
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5050)
