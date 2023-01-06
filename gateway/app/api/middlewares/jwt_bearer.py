from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.core.config import get_app_settings
from app.services.security import token_service
from app.errors.base import BaseErrors

settings = get_app_settings()


# Este solo se utiliza para fast api en la documentación automatica como ayuda
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_prefix_v1}/auth/access-token"
)


# Esta función permite obtener el usuario a partir del token
def get_user_id(
    token: str = Depends(reusable_oauth2)
) -> int:
    try:
        token_payload = token_service.decode_token(token)
    except (jwt.JWTError, BaseErrors):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_payload.sub

