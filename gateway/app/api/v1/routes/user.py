from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError, ContentTypeError

from app.schemas import UserCreate, UserUpdate
from app.network.services import database
from app.api.middlewares import http, jwt_bearer

router = APIRouter()


@router.post('/')
async def create_user(
    user: UserCreate,
    *,
    session: ClientSession = Depends(http.get_session)
):
    try:
        user, code = await database.user_service.post(session, data=user)
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
    return JSONResponse(content=user, status_code=code)


@router.get('/{id}')
async def get_user(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        user, code = await database.user_service.get(session, id=id,
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
    return JSONResponse(content=user, status_code=code)


@router.get('/')
async def get_users(
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        user, code = await database.user_service.get_multi(session,
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
    return JSONResponse(content=user, status_code=code)


@router.put('/{id}')
async def update_user(
    id: int,
    user: UserUpdate,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        user, code = await database.user_service.put(session, data=user, id=id,
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
    return JSONResponse(content=user, status_code=code)


@router.delete('/{id}')
async def delete_user(
    id: int,
    *,
    session: ClientSession = Depends(http.get_session),
    user_id: int = Depends(jwt_bearer.get_user_id)
):
    try:
        user, code = await database.user_service.delete(session, id=id,
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
    return JSONResponse(content=user, status_code=code)