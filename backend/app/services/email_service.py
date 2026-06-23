import logging
from aiosmtplib import send
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

from app.core.config import settings

logger = logging.getLogger(__name__)


env = Environment(loader=FileSystemLoader("app/templates"))

async def send_email(subject: str, recipients: list[str], html_content: str):
    """
    Asynchronously sends an HTML email via SMTP.
    """
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.warning("SMTP configuration is missing. Mocking email delivery to console.")
        logger.info(f"--- MOCK EMAIL DELIVERY TO {recipients} ---\nSubject: {subject}\n\nContent (HTML snippet):\n{html_content[:500]}...\n--------------------")
        return

    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(html_content, subtype="html")

    try:
        await send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True
        )
        logger.info(f"Successfully sent email: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipients}: {str(e)}")


async def send_intel_report(recipients: list[str], report_data: dict):
    """
    Sends the weekly digest intelligence report.
    """
    template = env.get_template("report.html")
    html_content = template.render(**report_data)
    await send_email("Weekly IntelGraphX AI Report", recipients, html_content)


async def send_red_alert(recipients: list[str], alert_data: dict):
    """
    Sends an immediate urgent alert regarding critical competitor changes.
    """
    template = env.get_template("alert.html")
    html_content = template.render(**alert_data)
    await send_email(f"URGENT: {alert_data.get('title')}", recipients, html_content)
