from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError

from app.schemas import IncomeCreate, IncomeUpdate
from app.network.services import database
from app.api.middlewares import http, jwt_bearer

router = APIRouter()


@router.post('/')
async def create_income(
    income: IncomeCreate,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income, code = await database.income_service.post(session, data=income,
                                                          headers={'user-id': str(user_id)})
    except ClientConnectorError:
        raise HTTPException(
            status_code=503,
            detail='Service is unavailable.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except ContentTypeError:
        raise HTTPException(
            status_code=500,
            detail='Service error.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return JSONResponse(content=income, status_code=code)


@router.get('/{id}')
async def get_income(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income, code = await database.income_service.get(session, id=id,
                                                         headers={'user-id': str(user_id)})
    except ClientConnectorError:
        raise HTTPException(
            status_code=503,
            detail='Service is unavailable.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except ContentTypeError:
        raise HTTPException(
            status_code=500,
            detail='Service error.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return JSONResponse(content=income, status_code=code)


@router.get('/')
async def get_incomes(
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id),
    skip: int = 0,
    limit: int = 100
):
    try:
        income, code = await database.income_service.get_multi(session,
                                                               headers={
                                                                   'user-id': str(user_id)},
                                                               skip=skip,
                                                               limit=limit)
    except ClientConnectorError:
        raise HTTPException(
            status_code=503,
            detail='Service is unavailable.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except ContentTypeError:
        raise HTTPException(
            status_code=500,
            detail='Service error.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return JSONResponse(content=income, status_code=code)


@router.put('/{id}')
async def update_income(
    id: int,
    income: IncomeUpdate,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income, code = await database.income_service.put(session, data=income, id=id,
                                                         headers={'user-id': str(user_id)})
    except ClientConnectorError:
        raise HTTPException(
            status_code=503,
            detail='Service is unavailable.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except ContentTypeError:
        raise HTTPException(
            status_code=500,
            detail='Service error.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return JSONResponse(content=income, status_code=code)


@router.delete('/{id}')
async def delete_income(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income, code = await database.income_service.delete(session, id=id,
                                                            headers={'user-id': str(user_id)})
    except ClientConnectorError:
        raise HTTPException(
            status_code=503,
            detail='Service is unavailable.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except ContentTypeError:
        raise HTTPException(
            status_code=500,
            detail='Service error.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return JSONResponse(content=income, status_code=code)
