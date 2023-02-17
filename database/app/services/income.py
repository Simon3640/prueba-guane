from .base import ServiceBase
from app.ABC.models import Income, User
from app.ABC.crud import ABCCRUDIncome
from app.schemas import IncomeCreate, IncomeUpdate


class IncomeService(ServiceBase[Income, IncomeCreate, IncomeUpdate, ABCCRUDIncome]):
    async def get_related(self, who: User, *, id: int) -> Income | None:
        return await self.crud.get_related(who, id=id)
