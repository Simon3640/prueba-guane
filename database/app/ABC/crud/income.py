from app.schemas import IncomeCreate, IncomeUpdate
from app.ABC.models import Income, User
from .crud import ABCCRUD


class ABCCRUDIncome(ABCCRUD[Income, IncomeCreate, IncomeUpdate]):
    async def get_related(self, who: User, *, id: int) -> Income | None:
        ...
