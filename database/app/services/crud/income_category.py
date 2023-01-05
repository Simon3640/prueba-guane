from tortoise.backends.base.client import BaseDBAsyncClient

from app.domain.models import IncomeCategory, User
from app.domain.schemas import IncomeCategoryCreate, IncomeCategoryUpdate, IncomeCategoryResponse
from app.domain.rules import IncomeCategoryRules
from .base import CRUDBase


class CRUDIncomeCategory(CRUDBase[IncomeCategory, IncomeCategoryCreate, IncomeCategoryUpdate, IncomeCategoryRules]):
    async def get(self, db: BaseDBAsyncClient, who: User, *, id: int) -> IncomeCategoryResponse | None:
        category = await (IncomeCategory.filter(id=id)
                          .using_db(_db=db)
                          .first()
                          .select_related('incomes'))
        self.rules.get(who=who, to=category)
        incomes = await category.incomes.all().using_db(db)
        return IncomeCategoryResponse(**category.__dict__, incomes=incomes)
    
    async def get_multi(
        self,
        db: BaseDBAsyncClient,
        who: User,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> list[IncomeCategory]:
        categories = IncomeCategory.all().using_db(_db=db)
        if not who.is_superuser:
            categories = categories.filter(user_id=who.id)
        return await categories.offset(skip).limit(limit)


income_category = CRUDIncomeCategory(IncomeCategory, IncomeCategoryRules())
