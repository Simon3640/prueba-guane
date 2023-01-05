from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt

from app.core.config import get_app_settings
from app.schemas import TokenPayload
from app.errors.token import token403

settings = get_app_settings()

class TokenService:
    def __init__(self):
        pass

    def create_access_token(
        self, subject: Union[str, Any], *, expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expires = datetime.utcnow() + expires_delta
        else:
            expires = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expires_minutes
            )
        token = jwt.encode(
            {"exp": expires, "sub": str(subject)},
            settings.secret_key._secret_value,
            algorithm=settings.algorithm
        )
        return token


    def decode_token(
        self,
        token: str
    ) -> TokenPayload:
        try:
            decoded_token = jwt.decode(
                token, settings.secret_key._secret_value, algorithms=[settings.algorithm])
            return TokenPayload(**decoded_token)
        except jwt.JWTError:
            raise token403


token_service = TokenService()