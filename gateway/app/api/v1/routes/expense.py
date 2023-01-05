from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError

from app.schemas import ExpenseCreate, ExpenseUpdate
from app.network.services import database
from app.api.middlewares import http, jwt_bearer

router = APIRouter()


@router.post('/')
async def create_expense(
    expense: ExpenseCreate,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense, code = await database.expense_service.post(session, data=expense,
                                                            headers={'user-id': user_id})
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
    return JSONResponse(content=expense, status_code=code)


@router.get('/{id}')
async def get_expense(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense, code = await database.expense_service.get(session, id=id,
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
    return JSONResponse(content=expense, status_code=code)


@router.get('/')
async def get_expenses(
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense, code = await database.expense_service.get_multi(session,
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
    return JSONResponse(content=expense, status_code=code)


@router.put('/{id}')
async def update_expense(
    id: int,
    expense: ExpenseUpdate,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense, code = await database.expense_service.put(session, data=expense, id=id,
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
    return JSONResponse(content=expense, status_code=code)


@router.delete('/{id}')
async def delete_expense(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense, code = await database.expense_service.delete(session, id=id,
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
    return JSONResponse(content=expense, status_code=code)
