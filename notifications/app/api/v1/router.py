from fastapi import APIRouter

from .routes import notification

api_route = APIRouter()

api_route.include_router(notification.router, prefix='/notification', tags=['notification'])