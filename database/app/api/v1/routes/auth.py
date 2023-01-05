from fastapi import APIRouter, Depends, HTTPException
from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.schemas import UserResponse, UserLogin
from app.domain.errors.base import BaseErrors
from app.services import crud
from app.api.middlewares import db

router = APIRouter()


@router.post('/', response_model=UserResponse)
async def authenticate(
    user_login: UserLogin,
    *,
    db: BaseDBAsyncClient = Depends(db.get_db)
) -> UserResponse:
    try:
        user = await crud.user.authenticate(
            db, username=user_login.username, password=user_login.password)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user
