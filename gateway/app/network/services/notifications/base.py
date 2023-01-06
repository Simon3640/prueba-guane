from typing import Generic, TypeVar, Type
from json import loads

from aiohttp import ClientSession
from async_timeout import timeout
from pydantic import BaseModel

from app.core.config import get_app_settings

settings = get_app_settings()

NotificationModel = TypeVar('NotificationModel', bound=BaseModel)


class ServiceBase(Generic[NotificationModel]):
    def __init__(self, url: str):
        self.url = url

    async def post(
        self,
        session: ClientSession,
        *,
        data: Type[NotificationModel]
    ):
        with timeout(settings.gateway_timeout):
            async with session.post(
                self.url,
                json=loads(data.json(exclude_unset=True))) as response:
                data = await response.json()
                return (data, response.status)