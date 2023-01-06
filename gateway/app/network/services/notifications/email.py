from .base import ServiceBase
from app.schemas import NotificationEmail
from app.core.config import get_app_settings

settings = get_app_settings()


class EmailService(ServiceBase[NotificationEmail]):
    pass


email_service = EmailService(settings.notifications_svc + 'notification/')