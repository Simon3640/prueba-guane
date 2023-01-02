from fastapi import APIRouter, Depends
from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.models import User
from app.api.middlewares.db import get_db
from app.services.crud import user

router = APIRouter()

@router.post('/')
def hello_world():
    return {'msg': 'Hello world'}


@router.get('/')
async def get_users(
    *,
    db: BaseDBAsyncClient = Depends(get_db)
):
    return await user.get_multi(db)