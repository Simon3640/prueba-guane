from fastapi import APIRouter, Depends, HTTPException, Header

from app.schemas import IncomeCreate, IncomeInDB, IncomeUpdate, Msg
from app.ABC.models import User
from app.helpers.loads.errors.base import BaseErrors
from app.services import income_service
from app.api.middlewares import user


router = APIRouter()


@router.post('/', response_model=IncomeInDB)
async def create_Income(
    income: IncomeCreate,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user)
) -> IncomeInDB:
    try:
        income = await income_service.create(current_user, obj_in=income)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return income


@router.get('/', response_model=list[IncomeInDB])
async def get_Incomes(
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[IncomeInDB]:
    try:
        incomes = await income_service.get_multi(current_user, skip=skip, limit=limit)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return incomes


@router.get('/{id}', response_model=IncomeInDB)
async def get_Income(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> IncomeInDB:
    try:
        income = await income_service.get(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.code, e.detail)
    return income


@router.put('/{id}', response_model=IncomeInDB)
async def update_Income(
    id: int,
    income: IncomeUpdate,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> IncomeInDB:
    try:
        income = await income_service.update(current_user, obj_in=income, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return income


@router.delete('/{id}', response_model=Msg)
async def delete_Income(
    id: int,
    *,
    user_id: int = Header(),
    current_user: User = Depends(user.get_current_user),
) -> Msg:
    try:
        income = await income_service.delete(current_user, id=id)
    except BaseErrors as e:
        raise HTTPException(e.detail, e.code)
    return {'msg': 'El gasto ha sido eliminado'}
