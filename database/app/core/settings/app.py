import logging
from typing import Any, Dict, Optional, Tuple, Union

from pydantic import PostgresDsn, validator, AnyHttpUrl

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
    title: str = "FastAPI prueba guane database"
    version: str = "1.0.0"
    api_prefix_v1: str = "/api/v1"

    # Cors Origins
    backend_cors_origins: list[AnyHttpUrl] = []

    # Lista de url de las que se permitirán requests
    @validator("backend_cors_origins", pre=True)
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # First Super User
    first_superemployee_password: str
    first_superemployee_last_names: str
    first_superemployee_names: str
    first_superemployee_email: str
    first_superemployee_nick_name: str

    # postgres
    postgres_server: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_uri: Optional[PostgresDsn] = None
    # En este validador de pydantic que nos sirve para asignar valores a ciertas variables
    # o también para hacer una validación mas rigurosa, de esta manera estamos generando el Dsn
    # por el que nos vamos a conectar a la base de datos de postgresql

    @validator("postgres_uri", pre=True)
    def validate_database_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        return PostgresDsn.build(
            scheme="postgres",
            user=values.get("postgres_user"),
            password=values.get("postgres_password"),
            host=values.get("postgres_server"),
            path=f"/{values.get('postgres_db')}",
        )

    # Loggin
    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True
        env_file_encoding = "utf-8"

    # El decorador property simplemente nos devolverá un diccionario con los datos de nuestra aplicación
    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
