from typing import Generic, TypeVar, Type

from aiohttp import ClientSession
from async_timeout import timeout
from pydantic import BaseModel

from app.core.config import get_app_settings
from app.core.logging import get_logging

settings = get_app_settings()
log = get_logging(__name__)

CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class ServiceBase(Generic[CreateSchemaType, UpdateSchemaType]):
    def __init__(self, url: str):
        self.url = url

    async def post(
        self,
        session: ClientSession,
        *,
        data: Type[CreateSchemaType],
        path: str | None = None,
        headers: dict | None = None
    ):
        with timeout(settings.gateway_timeout):
            url = self.url + path if path else self.url
            async with session.post(
                    url,
                    json=data.dict(exclude_unset=True, exclude_none=True),
                    headers=headers) as response:
                data = await response.json()
                log.debug(data)
                return (data, response.status)

    async def get(
        self,
        session: ClientSession,
        *,
        id: int,
        headers: dict | None = None
    ):
        with timeout(settings.gateway_timeout):
            async with session.get(
                    self.url + str(id),
                    headers=headers) as response:
                data = await response.json()
                return (data, response.status)

    async def get_multi(
        self,
        session: ClientSession,
        *,
        path: str | None = None,
        headers: dict | None = None
    ):
        url = self.url + path if path else self.url
        with timeout(settings.gateway_timeout):
            async with session.get(
                url,
                headers=headers) as response:
                data = await response.json()
                return (data, response.status)

    async def put(
        self,
        session: ClientSession,
        *,
        data: Type[UpdateSchemaType],
        id: int,
        headers: dict | None = None
    ):
        with timeout(settings.gateway_timeout):
            async with session.put(
                self.url + str(id),
                json=data.dict(exclude_unset=True, exclude_none=True),
                headers=headers) as response:
                data = await response.json()
                return (data, response.status)

    async def delete(
        self,
        session: ClientSession,
        *,
        id: int,
        headers: dict | None = None
    ):
        with timeout(settings.gateway_timeout):
            async with session.delete(
                self.url + str(id),
                headers=headers) as response:
                data = await response.json()
                return (data, response.status)
