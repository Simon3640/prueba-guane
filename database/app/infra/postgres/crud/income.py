from tortoise.transactions import in_transaction

from app.infra.postgres.models import Income, User
from app.helpers.loads.rules import IncomeRules
from app.schemas import IncomeCreate, IncomeUpdate
from .base import CRUDBase


class CRUDIncome(CRUDBase[Income, IncomeCreate, IncomeUpdate, IncomeRules]):
    async def get_related(self, who: User, *, id: int) -> Income | None:
        async with in_transaction() as db:
            income = (
                await Income.filter(id=id)
                .using_db(_db=db)
                .select_related("category")
                .first()
            )
            self.rules.get(who=who, to=income)
            return income

    async def get_multi(
        self, who: User, *, skip: int = 0, limit: int = 100
    ) -> list[Income]:
        async with in_transaction() as db:
            self.rules.get_multi(who=who)
            incomes = Income.all().using_db(_db=db)
            if not who.is_superuser:
                incomes = incomes.filter(category__user_id=who.id)
            return await incomes.offset(skip).limit(limit)


income = CRUDIncome(Income, IncomeRules())
