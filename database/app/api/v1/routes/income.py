from fastapi import APIRouter, Depends, HTTPException, Header
from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.schemas import IncomeCreate, IncomeInDB, IncomeUpdate, Msg
from app.domain.models import Income, User
from app.domain.errors.base import BaseErrors
from app.services import crud
from app.api.middlewares import db, user


router = APIRouter()


@router.post('/', response_model=IncomeInDB)
async def create_Income(
    income: IncomeCreate,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user)
) -> IncomeInDB:
    try:
        income = await crud.income.create(db, current_user, obj_in=income)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return income


@router.get('/', response_model=list[IncomeInDB])
async def get_Incomes(
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[IncomeInDB]:
    try:
        incomes = await crud.income.get_multi(db, current_user, skip=skip, limit=limit)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return incomes


@router.get('/{id}', response_model=IncomeInDB)
async def get_Income(
    id: int,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> IncomeInDB:
    try:
        income = await crud.income.get(db, current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return income


@router.put('/{id}', response_model=IncomeInDB)
async def update_Income(
    id: int,
    income: IncomeUpdate,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> IncomeInDB:
    try:
        db_obj = await crud.income.get(db, current_user, id=id)
        income = await crud.income.update(db, current_user,
                                            db_obj=db_obj, obj_in=income)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return income


@router.delete('/{id}', response_model=Msg)
async def delete_Income(
    id: int,
    *,
    user_id: int = Header(),
    db: BaseDBAsyncClient = Depends(db.get_db),
    current_user: User = Depends(user.get_current_user),
) -> Msg:
    try:
        # Execute get Rule
        income = await crud.income.get(db, current_user, id=id)
        income = await crud.income.delete(db, current_user, id=income.id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return {'msg': 'El gasto ha sido eliminado'}
