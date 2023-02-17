from fastapi import APIRouter, Depends, HTTPException, Header
from tortoise.backends.base.client import BaseDBAsyncClient

from app.schemas import UserCreate, UserUpdate, UserResponse, Msg
from app.ABC.models import User
from app.helpers.loads.errors.base import BaseErrors
from app.api.middlewares import user
from app.services import user_service
from app.core.logging import get_logging

router = APIRouter()
log = get_logging(__name__)


@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate) -> UserResponse:
    try:
        user = await user_service.create(obj_in=user)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user


@router.get("/", response_model=list[UserResponse])
async def get_users(
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100,
    active: bool | None = True,
) -> list[UserResponse]:
    log.debug(current_user.__dict__)
    try:
        users = await user_service.get_multi(
            current_user, skip=skip, limit=limit, active=active
        )
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return users


@router.get("/{id}", response_model=UserResponse)
async def get_user(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> UserResponse:
    try:
        user = await user_service.get(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user


@router.put("/{id}", response_model=UserResponse)
async def update_user(
    user: UserUpdate,
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> UserResponse:
    try:
        user_updated = await user_service.update(current_user, obj_in=user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return user_updated


@router.delete("/{id}", response_model=Msg)
async def delete_user(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> Msg:
    try:
        user = await user_service.delete(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return {"msg": "Usuario eliminado con éxito"}
