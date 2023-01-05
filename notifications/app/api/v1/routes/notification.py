from fastapi import APIRouter

from app.schemas import NotificationEmail
from app.services import email

router = APIRouter()


@router.post('/')
def hello(notification: NotificationEmail):
    email.expense_alert.apply_async(args=(notification.dict(exclude_unset=True), 'helper'))
    return notification