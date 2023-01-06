from time import sleep

from aiohttp import ClientSession

from app.schemas import NotificationEmail
from app.network.services.database import expense_category_service, user_service
from app.network.services.notifications import email_service
from app.core.logging import get_logging

log = get_logging(__name__)


async def calcule_expenses(session: ClientSession, *, id: int, headers: dict) -> None:
    sleep(0.1)
    category, code = await expense_category_service.get(session, id=id, headers=headers)

    if code != 200:
        return None

    expenses = category['expenses']
    total = sum(map(lambda x: x['value'], expenses))
    log.debug(total)
    if total >= category['budget'] * 0.9:
        sleep(0.1)
        user, code = await user_service.get(session,
                                            id=category['user_id'],
                                            headers={'user-id': str(category['user_id'])})
        data = NotificationEmail(email=user['email'], name=user['names'])
        await email_service.post(session, data=data)
    return None
