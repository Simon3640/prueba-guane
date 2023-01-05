from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError

from app.schemas import IncomeCategoryCreateBase, IncomeCategoryUpdate
from app.network.services import database
from app.api.middlewares import http, jwt_bearer

router = APIRouter()


@router.post('/')
async def create_income_category(
    income_category: IncomeCategoryCreateBase,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income_category, code = await database.income_category_service.post(session, data=income_category,
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
    return JSONResponse(content=income_category, status_code=code)


@router.get('/{id}')
async def get_income_category(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income_category, code = await database.income_category_service.get(session, id=id,
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
    return JSONResponse(content=income_category, status_code=code)


@router.get('/')
async def get_income_categorys(
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income_category, code = await database.income_category_service.get_multi(session,
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
    return JSONResponse(content=income_category, status_code=code)


@router.put('/{id}')
async def update_income_category(
    id: int,
    income_category: IncomeCategoryUpdate,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income_category, code = await database.income_category_service.put(session, data=income_category, id=id,
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
    return JSONResponse(content=income_category, status_code=code)


@router.delete('/{id}')
async def delete_income_category(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        income_category, code = await database.income_category_service.delete(session, id=id,
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
    return JSONResponse(content=income_category, status_code=code)
