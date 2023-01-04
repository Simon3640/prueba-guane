from fastapi import APIRouter, Depends, HTTPException, Header
from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.schemas import UserCreate, UserUpdate, UserResponse, Msg
from app.domain.models import User
from app.domain.errors.base import BaseErrors
from app.api.middlewares import db, user
from app.services import crud
from app.core.logging import get_logging

router = APIRouter()
log = get_logging(__name__)


@router.post('/', response_model=UserResponse)
async def create_user(
    user: UserCreate,
    *,
    db: BaseDBAsyncClient = Depends(db.get_db)
) -> UserResponse:
    try:
        user = await crud.user.create(db, obj_in=user)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user


@router.get('/', response_model=list[UserResponse])
async def get_users(
    *,
    db: BaseDBAsyncClient = Depends(db.get_db),
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100,
    active: bool | None = True
) -> list[UserResponse]:
    log.debug(current_user.__dict__)
    try:
        users = await crud.user.get_multi(db, current_user, skip=skip, limit=limit, active=active)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return users


@router.get('/{id}', response_model=UserResponse)
async def get_user(
    id: int,
    *,
    db: BaseDBAsyncClient = Depends(db.get_db),
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> UserResponse:
    try:
        user = await crud.user.get(db, current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user


@router.put('/{id}', response_model=UserResponse)
async def update_user(
    user: UserUpdate,
    id: int,
    *,
    db: BaseDBAsyncClient = Depends(db.get_db),
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> UserResponse:
    try:
        db_obj = await crud.user.get(db, id=id)
        user_updated = await crud.user.update(db, current_user, obj_in=user, db_obj=db_obj)
        log.debug(user_updated)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user_updated


@router.delete('/{id}', response_model=Msg)
async def delete_user(
    id: int,
    *,
    db: BaseDBAsyncClient = Depends(db.get_db),
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> Msg:
    try:
        user = await crud.user.delete(db, current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return {'msg': 'Usuario eliminado con éxito'}
