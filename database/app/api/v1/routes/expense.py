from fastapi import APIRouter, Depends, HTTPException, Header
from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.schemas import ExpenseCreate, ExpenseInDB, ExpenseUpdate, Msg
from app.domain.models import Expense, User
from app.domain.errors.base import BaseErrors
from app.services import crud
from app.api.middlewares import db, user


router = APIRouter()


@router.post('/', response_model=ExpenseInDB)
async def create_expense(
    expense: ExpenseCreate,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user)
) -> ExpenseInDB:
    try:
        expense = await crud.expense.create(db, current_user, obj_in=expense)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return expense


@router.get('/', response_model=list[ExpenseInDB])
async def get_expenses(
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[ExpenseInDB]:
    try:
        expenses = await crud.expense.get_multi(db, current_user, skip=skip, limit=limit)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return expenses


@router.get('/{id}', response_model=ExpenseInDB)
async def get_expense(
    id: int,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> ExpenseInDB:
    try:
        expense = await crud.expense.get(db, current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return expense


@router.put('/{id}', response_model=ExpenseInDB)
async def update_expense(
    id: int,
    expense: ExpenseUpdate,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> ExpenseInDB:
    try:
        db_obj = await crud.expense.get(db, current_user, id=id)
        expense = await crud.expense.update(db, current_user,
                                            db_obj=db_obj, obj_in=expense)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return expense


@router.delete('/{id}', response_model=Msg)
async def delete_expense(
    id: int,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> Msg:
    try:
        expense = await crud.expense.delete(db, current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return {'msg': 'El gasto ha sido eliminado'}
