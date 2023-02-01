from fastapi import APIRouter, Depends, HTTPException, Header

from app.schemas import ExpenseCreate, ExpenseInDB, ExpenseUpdate, Msg
from app.ABC.models import User
from app.helpers.loads.errors.base import BaseErrors
from app.services import expense_service
from app.api.middlewares import user


router = APIRouter()


@router.post('/', response_model=ExpenseInDB)
async def create_expense(
    expense: ExpenseCreate,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user)
) -> ExpenseInDB:
    try:
        expense = await expense_service.create(current_user, obj_in=expense)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return expense


@router.get('/', response_model=list[ExpenseInDB])
async def get_expenses(
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[ExpenseInDB]:
    try:
        expenses = await expense_service.get_multi(current_user, skip=skip, limit=limit)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return expenses


@router.get('/{id}', response_model=ExpenseInDB)
async def get_expense(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> ExpenseInDB:
    try:
        expense = await expense_service.get(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return expense


@router.put('/{id}', response_model=ExpenseInDB)
async def update_expense(
    id: int,
    expense: ExpenseUpdate,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> ExpenseInDB:
    try:
        expense = await expense_service.update(current_user, obj_in=expense, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return expense


@router.delete('/{id}', response_model=Msg)
async def delete_expense(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> Msg:
    try:
        expense = await expense_service.delete(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return {'msg': 'El gasto ha sido eliminado'}
