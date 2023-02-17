import pytest

from app.services import user_service
from app.infra.postgres.crud.user import CRUDUser
from app.schemas import UserCreate, UserUpdate
from tests.utils.data import user_john, user_simon, user_john_create, user_simon_create
from tests.utils.classes import User


@pytest.mark.asyncio
async def test_user(monkeypatch: pytest.MonkeyPatch):
    # Mock methods
    async def mock_get_middleware(self, id: int) -> User:
        return User(**user_john)

    async def mock_get_by_email(self, email: str) -> User:
        return User(**user_simon)

    async def mock_get_multi(
        self, who: User, *, skip: int = 0, limit: int = 0, active: bool = True
    ) -> User:
        return [User(**user_john), User(**user_simon)]

    async def mock_create(self, *, obj_in: UserCreate) -> User:
        user = obj_in.dict()
        del user["password"]
        user["hashed_password"] = "super hashed password"
        return User(**user, id=3)

    async def mock_update(self, who: User, *, obj_in: UserUpdate, id: int) -> User:
        return User(**obj_in.dict(), id=id)

    async def mock_authenticate(self, *, username: str, password: str) -> User | None:
        return None

    # Patch
    monkeypatch.setattr(CRUDUser, "get_middleware", mock_get_middleware)
    monkeypatch.setattr(CRUDUser, "get_by_email", mock_get_by_email)
    monkeypatch.setattr(CRUDUser, "get_multi", mock_get_multi)
    monkeypatch.setattr(CRUDUser, "create", mock_create)
    monkeypatch.setattr(CRUDUser, "update", mock_update)
    monkeypatch.setattr(CRUDUser, "authenticate", mock_authenticate)

    response_middleware = await user_service.get_middleware(2)

    assert response_middleware.username == "John0username"

    response_get_by_email = await user_service.get_by_email("fake@testing.com")

    assert response_get_by_email.username == "Simon0username"

    response_get_multi = await user_service.get_multi(response_get_by_email)

    assert response_get_multi[0].username == "John0username"
    assert response_get_multi[1].username == "Simon0username"

    response_create = await user_service.create(obj_in=UserCreate(**user_john_create))

    assert response_create.hashed_password == "super hashed password"

    response_update = await user_service.update(
        response_create, obj_in=UserUpdate(**user_simon_create), id=3
    )

    assert response_update.username == "Simon0username".upper()

    response_authenticate = await user_service.authenticate(
        username="username", password="password"
    )

    assert response_authenticate is None
