from fastapi import FastAPI
from app.routes import user_routes


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_routes.router)
    return app
