from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from aiohttp import ClientSession

from app.schemas import Token, UserLogin
from app.services.security import token_service
from app.network.services import database
from app.core.config import get_app_settings
from app.api.middlewares import http
from app.errors.base import BaseErrors

settings = get_app_settings()

router = APIRouter()


# Route for authenticate users, authentication can be with email or identification number
@router.post("/access-token", response_model=Token)
async def login_access_token(
    session: ClientSession = Depends(http.get_session), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests

        authentication can be with email or username
    """
    try:
        data = UserLogin(username=form_data.username, password=form_data.password)
        user, code = await database.user_service.authenticate(session, data=data)
        if code != 200:
            raise HTTPException(
                status_code=401,
                detail="El correo o la contraseña están erradas",
            )
        minutes = settings.access_token_expires_minutes
        access_token_expires = timedelta(
            minutes=minutes)
        access_token = token_service.create_access_token(
            user['id'], expires_delta=access_token_expires
        )
        response = Token(access_token=access_token,
                                 token_type='bearer', expires=minutes/24/60)
    except BaseErrors as e:
        raise HTTPException(status_code=e.code, detail=e.detail)
    return response