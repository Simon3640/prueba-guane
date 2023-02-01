from tortoise.transactions import in_transaction

from app.infra.postgres.models import IncomeCategory, User
from app.schemas import IncomeCategoryCreate, IncomeCategoryUpdate, IncomeCategoryResponse
from app.helpers.loads.rules import IncomeCategoryRules
from .base import CRUDBase


class CRUDIncomeCategory(CRUDBase[IncomeCategory, IncomeCategoryCreate, IncomeCategoryUpdate, IncomeCategoryRules]):
    async def get_related(self, who: User, *, id: int) -> IncomeCategoryResponse | None:
        async with in_transaction() as db:
            category = await (IncomeCategory.filter(id=id)
                            .using_db(_db=db)
                            .first()
                            .select_related('incomes'))
            self.rules.get(who=who, to=category)
            incomes = await category.incomes.all().using_db(db)
            return IncomeCategoryResponse(**category.__dict__, incomes=incomes)
    
    async def get_multi(
        self,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> list[IncomeCategory]:
        async with in_transaction() as db:
            self.rules.get_multi(who=who)
            categories = IncomeCategory.all().using_db(_db=db)
            if not who.is_superuser:
                categories = categories.filter(user_id=who.id)
            return await categories.offset(skip).limit(limit)


income_category = CRUDIncomeCategory(IncomeCategory, IncomeCategoryRules())
