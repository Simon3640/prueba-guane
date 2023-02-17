from typing import TypeVar

from pydantic import BaseModel
from tortoise.models import Model

ModelType = TypeVar("ModelType", bound=Model)

UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
