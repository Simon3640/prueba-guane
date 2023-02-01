from fastapi import APIRouter, Depends, HTTPException, Header

from app.schemas import (IncomeCategoryCreate,
                         IncomeCategoryInDB,
                         IncomeCategoryCreateBase,
                         IncomeCategoryUpdate,
                         IncomeCategoryResponse,
                         Msg)
from app.ABC.models import User
from app.helpers.loads.errors.base import BaseErrors
from app.services import income_category_service
from app.api.middlewares import user


router = APIRouter()


@router.post('/', response_model=IncomeCategoryInDB)
async def create_category(
    category: IncomeCategoryCreateBase,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user)
) -> IncomeCategoryInDB:
    try:
        obj_in = IncomeCategoryCreate(
            **category.dict(exclude_unset=True), user_id=current_user.id)
        category = await income_category_service.create(current_user, obj_in=obj_in)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return category


@router.get('/', response_model=list[IncomeCategoryInDB])
async def get_categories(
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[IncomeCategoryInDB]:
    try:
        categories = await income_category_service.get_multi(current_user, skip=skip, limit=limit)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return categories


@router.get('/{id}', response_model=IncomeCategoryResponse)
async def get_category(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> IncomeCategoryResponse:
    try:
        category = await income_category_service.get_related(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return category


@router.put('/{id}', response_model=IncomeCategoryInDB)
async def update_category(
    id: int,
    category: IncomeCategoryUpdate,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> IncomeCategoryInDB:
    try:
        category = await income_category_service.update(current_user, obj_in=category, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return category


@router.delete('/{id}', response_model=Msg)
async def delete_category(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> Msg:
    try:
        category = await income_category_service.delete(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return {'msg': 'La categoría ha sido eliminado'}
