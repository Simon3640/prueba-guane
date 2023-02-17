from fastapi import APIRouter, Depends, HTTPException, Header

from app.schemas import (
    ExpenseCategoryCreate,
    ExpenseCategoryInDB,
    ExpenseCategoryCreateBase,
    ExpenseCategoryUpdate,
    ExpenseCategoryResponse,
    Msg,
)
from app.ABC.models import User
from app.helpers.loads.errors.base import BaseErrors
from app.services import expense_category_service
from app.api.middlewares import user


router = APIRouter()


@router.post("/", response_model=ExpenseCategoryInDB)
async def create_category(
    category: ExpenseCategoryCreateBase,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user)
) -> ExpenseCategoryInDB:
    try:
        obj_in = ExpenseCategoryCreate(
            **category.dict(exclude_unset=True), user_id=current_user.id
        )
        category = await expense_category_service.create(current_user, obj_in=obj_in)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return category


@router.get("/", response_model=list[ExpenseCategoryInDB])
async def get_categories(
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100
) -> list[ExpenseCategoryInDB]:
    try:
        categories = await expense_category_service.get_multi(
            current_user, skip=skip, limit=limit
        )
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return categories


@router.get("/{id}", response_model=ExpenseCategoryResponse)
async def get_category(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user)
) -> ExpenseCategoryResponse:
    try:
        category = await expense_category_service.get_prefetch(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return category


@router.put("/{id}", response_model=ExpenseCategoryInDB)
async def update_category(
    id: int,
    category: ExpenseCategoryUpdate,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user)
) -> ExpenseCategoryInDB:
    try:
        category = await expense_category_service.update(
            current_user, obj_in=category, id=id
        )
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return category


@router.delete("/{id}", response_model=Msg)
async def delete_category(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user)
) -> Msg:
    try:
        category = await expense_category_service.delete(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return {"msg": "La categoría ha sido eliminado"}
