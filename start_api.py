import uvicorn
from fastapi import FastAPI

from src.router.home_router import router as home_router
from src.router.user_router import router as user_router

app = FastAPI()


def setup_router() -> None:
    app.include_router(home_router)
    app.include_router(user_router, prefix='/v1')


def configure() -> None:
    setup_router()


configure()
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
