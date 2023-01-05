import smtplib

from jinja2 import Environment, FileSystemLoader
from email.message import EmailMessage

from .templates import templatesdir
from app.core.celery_worker import celery
from app.schemas import NotificationEmail
from app.core.config import get_app_settings

settings = get_app_settings()

@celery.task
def expense_alert(data: dict, help: str | None):
    env = Environment(loader=FileSystemLoader(templatesdir))
    template = env.get_template('expense.warn.html.j2')
    render = template.render(data)

    msg = EmailMessage()
    msg['Subject'] = 'Alerta gastos'
    msg['From'] = settings.smtp_from_email
    msg['To'] = data['email']
    msg.set_content(
        render,
        subtype='html'
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as smtp:
        smtp.login(settings.smtp_from_email, settings.smtp_user_password._secret_value)
        smtp.send_message(msg)