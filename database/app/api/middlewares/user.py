from fastapi import Request, HTTPException

from app.services import user_service
from app.core.logging import get_logging
from app.ABC.models import User

log = get_logging(__name__)


async def get_current_user(request: Request) -> User:
    user_id = request.headers["user-id"]
    if user_id is None:
        raise HTTPException(403, "No se pudieron validar tus credenciales")
    return await user_service.get_middleware(user_id)
