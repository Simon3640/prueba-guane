from fastapi import APIRouter, Depends, HTTPException
from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.schemas import UserCreate, UserUpdate, UserResponse, Msg
from app.domain.errors.base import BaseErrors
from app.api.middlewares.db import get_db
from app.services import crud
from app.core.logging import get_logging

router = APIRouter()
log = get_logging(__name__)


@router.post('/', response_model=UserResponse)
async def create_user(
    user: UserCreate,
    *,
    db: BaseDBAsyncClient = Depends(get_db)
) -> UserResponse:
    try:
        user = await crud.user.create(db, user)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user


@router.get('/', response_model=list[UserResponse])
async def get_users(
    *,
    db: BaseDBAsyncClient = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    active: bool | None = True
) -> list[UserResponse]:
    try:
        users = await crud.user.get_multi(db, skip=skip, limit=limit, active=active)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return users


@router.get('/{id}', response_model=UserResponse)
async def get_user(
    id: int,
    *,
    db: BaseDBAsyncClient = Depends(get_db)
) -> UserResponse:
    try:
        user = await crud.user.get(db, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user


@router.put('/{id}', response_model=UserResponse)
async def update_user(
    user: UserUpdate,
    id: int,
    *,
    db: BaseDBAsyncClient = Depends(get_db)
) -> UserResponse:
    try:
        db_obj = await crud.user.get(db, id=id)
        user_updated = await crud.user.update(db, obj_in=user, db_obj=db_obj)
        log.debug(user_updated)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user_updated


@router.delete('/{id}', response_model=Msg)
async def delete_user(
    id: int,
    *,
    db: BaseDBAsyncClient = Depends(get_db)
) -> Msg:
    try:
        user = await crud.user.delete(db, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return {'msg': 'Usuario eliminado con éxito'}
