import pytest

from app.services import income_service
from app.infra.postgres.crud.income import CRUDIncome
from tests.utils.classes import User, Income
from tests.utils.data import income_1, user_simon


@pytest.mark.asyncio
async def test_income(monkeypatch: pytest.MonkeyPatch):
    # Mock methods
    async def mock_get_related(self, who: User, * , id: int) -> Income | None:
        return Income(**income_1)

    monkeypatch.setattr(CRUDIncome, 'get_related', mock_get_related)

    user = User(**user_simon)
    response_income = await income_service.get_related(user, id=1)

    assert response_income.name == 'rent'