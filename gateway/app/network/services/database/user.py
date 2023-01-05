from aiohttp import ClientSession
from async_timeout import timeout

from .base import ServiceBase
from app.schemas import UserCreate, UserUpdate, UserLogin
from app.core.config import get_app_settings

settings = get_app_settings()


class UserService(ServiceBase[UserCreate, UserUpdate]):
    async def authenticate(
        self,
        session: ClientSession,
        *,
        data: UserLogin
    ):
        with timeout(settings.gateway_timeout):
            async with session.post(
                    settings.database_svc + 'auth/',
                    json=data.dict(exclude_unset=True, exclude_none=True)) as response:
                data = await response.json()
                return (data, response.status)


user_service = UserService(settings.database_svc + 'user/')
