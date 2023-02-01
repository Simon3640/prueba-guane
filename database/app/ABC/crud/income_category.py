from app.schemas import IncomeCategoryCreate, IncomeCategoryUpdate
from app.ABC.models import IncomeCategory, User
from .crud import ABCCRUD


class ABCCRUDIncomeCategory(ABCCRUD[IncomeCategory, IncomeCategoryCreate, IncomeCategoryUpdate]):
    async def get_related(self, who: User, *, id: int) -> IncomeCategory | None:
        ...
