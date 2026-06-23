from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertInDBBase

router = APIRouter()

@router.get("/", response_model=List[AlertInDBBase])
async def read_alerts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Return all intelligence alerts, newest first."""
    result = await db.execute(
        select(Alert).order_by(Alert.created_at.desc()).offset(skip).limit(limit)
    )
    alerts = result.scalars().all()
    return alerts

@router.post("/{alert_id}/resolve", response_model=AlertInDBBase)
async def resolve_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    """Mark an alert as approved / resolved after human review and resume pipeline."""
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.is_approved = True
    await db.commit()
    await db.refresh(alert)
    
    # Resume the LangGraph pipeline for this competitor
    try:
        from app.api.endpoints.pipeline import resume_pipeline
        from fastapi import BackgroundTasks
        bt = BackgroundTasks()
        await resume_pipeline(alert.competitor_id, bt)
        # We don't execute bt here since we aren't returning it, so we'll just fire it manually or let the caller know.
        # Actually, since we're in the router, we can just await the background task function directly or fire and forget.
        import asyncio
        for task in bt.tasks:
            asyncio.create_task(task.func(*task.args, **task.kwargs))
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Failed to trigger pipeline resume: {e}")

    return alert

@router.post("/{alert_id}/email")
async def send_alert_email(alert_id: int, db: AsyncSession = Depends(get_db)):
    """Manually dispatch this alert via email to the head of strategy."""
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    # In a real environment, you would use smtplib here to send via SendGrid, SES, or SMTP.
    # We will log the email dispatch for the demo.
    import logging
    import smtplib
    from email.message import EmailMessage
    import os

    logger = logging.getLogger(__name__)
    
    target_email = "vishnus202004@gmail.com"
    email_subject = f"URGENT {alert.severity} ALERT: {alert.title}"
    email_body = f"An intelligence alert requires your attention.\n\nDescription:\n{alert.description}"
    
    # 1. Log the dispatch attempt
    logger.info(f"========== DISPATCHING EMAIL ==========")
    logger.info(f"To: {target_email}")
    logger.info(f"Subject: {email_subject}")
    logger.info(f"=======================================")

    # 2. Attempt real SMTP dispatch if credentials exist
    from dotenv import load_dotenv
    load_dotenv()
    
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    
    if smtp_user and smtp_pass:
        try:
            msg = EmailMessage()
            msg.set_content(email_body)
            msg['Subject'] = email_subject
            msg['From'] = smtp_user
            msg['To'] = target_email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            logger.info("Real email successfully sent via Gmail SMTP.")
            return {"message": f"Real email dispatched to {target_email}!", "subject": email_subject}
        except Exception as e:
            logger.error(f"Failed to send real email: {e}")
            return {"message": f"Email failed. Check your SMTP credentials in .env.", "error": str(e)}
    else:
        logger.warning("SMTP_USER and SMTP_PASS not found in .env. Falling back to mocked log dispatch.")
        return {
            "message": f"Simulated dispatch to {target_email}. Add SMTP_USER and SMTP_PASS to .env to send real emails.",
            "subject": email_subject
        }

