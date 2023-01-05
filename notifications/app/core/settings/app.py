import logging
from typing import Any

from pydantic import validator, AnyHttpUrl, RedisDsn, SecretStr

from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    # En esta clase de pydantic nos dedicamos a generar la configuración de la aplicación,
    # pydantic automaticammente leerá las variables de entorno con las que encuentre similitud
    # FastApi Args
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI prueba guane gateway"
    version: str = "1.0.0"
    api_prefix_v1: str = "/api/v1"

    # redis 
    redis_server: str
    redis_path: str
    redis_uri: str | None = None

    # SMTP
    smtp_user_email: str
    smtp_user_password: SecretStr
    smtp_host_email: str
    smtp_port_email: int
    smtp_from_email: str

    @validator("redis_uri", pre=True)
    def validate_redis_uri(cls, v: str | None, values: dict[str, Any]) -> Any:
        return RedisDsn.build(
            scheme="redis",
            host=values.get('redis_server'),
            path=f"/{values.get('redis_path')}"
        )

    # Cors Origins
    backend_cors_origins: list[AnyHttpUrl] = []

    # Lista de url de las que se permitirán requests
    @validator("backend_cors_origins", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Loggin
    logging_level: int = logging.INFO
    loggers: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True
        env_file_encoding = 'utf-8'

    # El decorador property simplemente nos devolverá un diccionario con los datos de nuestra aplicación
    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
