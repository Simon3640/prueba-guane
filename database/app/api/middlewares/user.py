from fastapi import Depends, Request, HTTPException
from tortoise.backends.base.client import BaseDBAsyncClient

from .db import get_db
from app.services import crud
from app.core.logging import get_logging
from app.domain.models import User

log = get_logging(__name__)


async def get_current_user(request: Request, db: BaseDBAsyncClient = Depends(get_db)) -> User:
    user_id = request.headers['user-id']
    if user_id is None:
        raise HTTPException(403, 'No se pudieron validar tus credenciales')
    return await crud.user.get_middleware(db, user_id)