from fastapi import APIRouter, HTTPException

from app.schemas import UserResponse, UserLogin
from app.helpers.loads.errors.base import BaseErrors
from app.services import user_service
from app.api.middlewares import db

router = APIRouter()


@router.post('/', response_model=UserResponse)
async def authenticate(
    user_login: UserLogin,
) -> UserResponse:
    try:
        user = await user_service.authenticate(username=user_login.username, password=user_login.password)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user
