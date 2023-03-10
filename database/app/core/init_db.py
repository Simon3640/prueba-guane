from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import get_app_settings


settings = get_app_settings()


def get_tortoise_config() -> dict:
    config = {
        "connections": settings.postgres_uri,
        "apps": {
            "models": {
                "models": ["app.infra.postgres.models"],
                "default_connection": "default",
            }
        },
    }
    return config


def register_db(app: FastAPI, db_url: str = None):
    db_url = db_url or settings.postgres_uri
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["app.infra.postgres.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
