from fastapi import APIRouter, Depends, HTTPException, Header
from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.schemas import (ExpenseCategoryCreate,
                                ExpenseCategoryInDB,
                                ExpenseCategoryCreateBase,
                                ExpenseCategoryUpdate,
                                ExpenseCategoryResponse,
                                Msg)
from app.domain.models import User
from app.domain.errors.base import BaseErrors
from app.services import crud
from app.api.middlewares import db, user


router = APIRouter()


@router.post('/', response_model=ExpenseCategoryInDB)
async def create_category(
    category: ExpenseCategoryCreateBase,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user)
) -> ExpenseCategoryInDB:
    try:
        obj_in = ExpenseCategoryCreate(
            **category.dict(exclude_unset=True), user_id=current_user.id)
        category = await crud.expense_category.create(db, current_user, obj_in=obj_in)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return category


@router.get('/', response_model=list[ExpenseCategoryInDB])
async def get_categories(
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[ExpenseCategoryInDB]:
    try:
        categories = await crud.expense_category.get_multi(db, current_user, skip=skip, limit=limit)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return categories


@router.get('/{id}', response_model=ExpenseCategoryResponse)
async def get_category(
    id: int,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> ExpenseCategoryResponse:
    try:
        category = await crud.expense_category.get(db, current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return category


@router.put('/{id}', response_model=ExpenseCategoryInDB)
async def update_category(
    id: int,
    category: ExpenseCategoryUpdate,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> ExpenseCategoryInDB:
    try:
        db_obj = await crud.expense_category.get(db, current_user, id=id)
        category = await crud.expense_category.update(db, current_user,
                                                      db_obj=db_obj, obj_in=category)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return category


@router.delete('/{id}', response_model=Msg)
async def delete_category(
    id: int,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> Msg:
    try:
        category = await crud.expense_category.delete(db, current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return {'msg': 'La categoría ha sido eliminado'}
