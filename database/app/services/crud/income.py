from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.models import Income, User
from app.domain.rules import IncomeRules
from app.domain.schemas import IncomeCreate, IncomeUpdate
from .base import CRUDBase
from app.core.logging import get_logging

log = get_logging(__name__)


class CRUDIncome(CRUDBase[Income, IncomeCreate, IncomeUpdate, IncomeRules]):
    async def get(self, db: BaseDBAsyncClient, who: User, *, id: int) -> Income | None:
        income = await Income.filter(id=id).using_db(_db=db).select_related('category').first()
        self.rules.get(who=who, to=income)
        return income

    async def get_multi(
        self,
        db: BaseDBAsyncClient,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> list[Income]:
        incomes = Income.all().using_db(_db=db)
        if not who.is_superuser:
            incomes = incomes.filter(category__user_id=who.id)
        return await incomes.offset(skip).limit(limit)


income = CRUDIncome(Income, IncomeRules())
