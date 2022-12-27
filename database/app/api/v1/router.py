from fastapi import APIRouter

from app.api.v1.routes import user

api_route = APIRouter()

api_route.include_router(user.router, prefix='/user', tags=['user'])
