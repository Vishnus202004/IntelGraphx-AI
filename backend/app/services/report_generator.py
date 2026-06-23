import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.models.prediction import Prediction
from app.models.alert import Alert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def generate_weekly_report_pdf(db: AsyncSession, filepath: str):
    """
    Generate a PDF executive summary containing recent alerts and predictions.
    """
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("IntelGraphX AI - Weekly Battle Card", styles['Title']))
    story.append(Spacer(1, 12))

    # Fetch Alerts
    story.append(Paragraph("Recent Intelligence Alerts", styles['Heading2']))
    alert_result = await db.execute(select(Alert).order_by(Alert.created_at.desc()).limit(10))
    alerts = alert_result.scalars().all()
    
    if not alerts:
        story.append(Paragraph("No active alerts generated this week.", styles['Normal']))
    else:
        for a in alerts:
            story.append(Paragraph(f"<b>[{a.severity}]</b> {a.title}", styles['Normal']))
            story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))

    # Fetch Predictions
    story.append(Paragraph("AI Strategic Forecasts", styles['Heading2']))
    pred_result = await db.execute(select(Prediction).order_by(Prediction.created_at.desc()).limit(5))
    preds = pred_result.scalars().all()

    if not preds:
        story.append(Paragraph("No predictions generated this week.", styles['Normal']))
    else:
        for p in preds:
            story.append(Paragraph(f"<b>Confidence {round(p.confidence * 100)}%:</b> {p.content}", styles['Normal']))
            story.append(Spacer(1, 6))

    doc.build(story)
    return filepath
