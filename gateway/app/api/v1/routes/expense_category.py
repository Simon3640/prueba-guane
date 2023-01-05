from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError

from app.schemas import ExpenseCategoryCreateBase, ExpenseCategoryUpdate
from app.network.services import database
from app.api.middlewares import http, jwt_bearer

router = APIRouter()


@router.post('/')
async def create_expense_category(
    expense_category: ExpenseCategoryCreateBase,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense_category, code = await (database
                                        .expense_category_service
                                        .post(session, data=expense_category,
                                              headers={'user-id': str(user_id)}))
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
    return JSONResponse(content=expense_category, status_code=code)


@router.get('/{id}')
async def get_expense_category(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense_category, code = await (database
                                        .expense_category_service
                                        .get(session, id=id,
                                             headers={'user-id': str(user_id)}))
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
    return JSONResponse(content=expense_category, status_code=code)


@router.get('/')
async def get_expense_categorys(
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id),
    skip: int = 0,
    limit: int = 100
):
    try:
        expense_category, code = await (database
                                        .expense_category_service
                                        .get_multi(session,
                                                   headers={
                                                       'user-id': str(user_id)},
                                                   skip=skip,
                                                   limit=limit))
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
    return JSONResponse(content=expense_category, status_code=code)


@router.put('/{id}')
async def update_expense_category(
    id: int,
    expense_category: ExpenseCategoryUpdate,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense_category, code = await (database
                                        .expense_category_service
                                        .put(session, data=expense_category, id=id,
                                             headers={'user-id': str(user_id)}))
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
    return JSONResponse(content=expense_category, status_code=code)


@router.delete('/{id}')
async def delete_expense_category(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        expense_category, code = await (database
                                        .expense_category_service
                                        .delete(session, id=id,
                                                headers={'user-id': str(user_id)}))
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
    return JSONResponse(content=expense_category, status_code=code)
