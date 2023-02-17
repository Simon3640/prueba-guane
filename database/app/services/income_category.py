from .base import ServiceBase
from app.ABC.models import IncomeCategory, User
from app.ABC.crud import ABCCRUDIncomeCategory
from app.schemas import (
    IncomeCategoryCreate,
    IncomeCategoryUpdate,
    IncomeCategoryResponse,
)


class IncomeCategoryService(
    ServiceBase[
        IncomeCategory,
        IncomeCategoryCreate,
        IncomeCategoryUpdate,
        ABCCRUDIncomeCategory,
    ]
):
    async def get_related(self, who: User, *, id: int) -> IncomeCategoryResponse | None:
        return await self.crud.get_related(who, id=id)
