import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.future import select

from app.services.scraper import detect_webpage_changes
from app.services.news import fetch_news_via_google_rss
from app.services.vector_store import store_scraped_content
from app.agents.graph import agent_pipeline
from app.core.database import async_session_maker
from app.models.competitor import Competitor

logger = logging.getLogger(__name__)


async def automated_intelligence_job():
    """
    Background job that autonomously monitors all tracked competitors,
    embeds new content into ChromaDB, then invokes the Groq LangGraph pipeline
    and stores the resulting Alerts and Predictions in the database.
    Triggered every 6 hours by APScheduler.
    """
    logger.info("=== AUTOMATED INTELLIGENCE JOB STARTED ===")

    async with async_session_maker() as db:
        result = await db.execute(select(Competitor).where(Competitor.is_active == True))
        competitors = result.scalars().all()

        if not competitors:
            logger.info("No active competitors found. Skipping intelligence cycle.")
            return

        for comp in competitors:
            logger.info(f"--- Processing: {comp.name} ({comp.domain}) ---")

            try:
                # 1. Scrape the target URL and detect structural changes
                scrape_result = await detect_webpage_changes(
                    db=db,
                    competitor_id=comp.id,
                    url=comp.domain
                )
                has_changed   = scrape_result["has_changed"]
                scraped_text  = scrape_result["content"]

                if not has_changed:
                    logger.info(f"No changes detected for {comp.name}. Skipping analysis.")
                    continue

                logger.info(f"Change detected for {comp.name}. Running full intelligence cycle.")

                # 2. Embed the scraped content into ChromaDB for future RAG retrieval
                await store_scraped_content(
                    competitor_id=comp.id,
                    url=comp.domain,
                    content=scraped_text
                )

                # 3. Fetch live Google News
                news_items = await fetch_news_via_google_rss(comp.name)

                # 4. Build the complete AgentState for the LangGraph pipeline
                thread_id    = f"comp-{comp.id}-scheduler"
                config       = {"configurable": {"thread_id": thread_id}}
                initial_state = {
                    "competitor_id":       comp.id,
                    "competitor_name":     comp.name,
                    "url":                 comp.domain,
                    "has_changed":         has_changed,
                    "scraped_content":     scraped_text,
                    "recent_news":         news_items,
                    "relevant_chunks":     [],
                    "analysis_summary":    "",
                    "threat_score":        0,
                    "recommendation":      "",
                    "reflection_feedback": "",
                    "analysis_attempts":   0,
                    "is_analysis_valid":   False,
                    "predicted_action":    "",
                    "confidence_score":    0.0,
                    "alert_severity":      "",
                    "alert_title":         "",
                    "messages":            []
                }

                # 5. Run the pipeline up to the Human-in-the-Loop interrupt (before alert node)
                await agent_pipeline.ainvoke(initial_state, config=config)
                logger.info(f"Pipeline completed for {comp.name} — paused at HITL checkpoint.")

            except Exception as e:
                logger.error(f"Pipeline failed for {comp.name}: {e}", exc_info=True)
                continue

    logger.info("=== AUTOMATED INTELLIGENCE JOB COMPLETE ===")


# Initialize the scheduler
scheduler = AsyncIOScheduler()

async def automated_weekly_report_job():
    """
    Background job that runs once a week to aggregate competitor insights
    and emails a weekly digest to the Head of Strategy.
    """
    from app.services.email_service import send_intel_report
    from app.models.alert import Alert
    from app.models.prediction import Prediction
    
    logger.info("=== WEEKLY REPORT JOB STARTED ===")
    async with async_session_maker() as db:
        comp_result = await db.execute(select(Competitor).where(Competitor.is_active == True))
        competitors = comp_result.scalars().all()
        
        report_competitors = []
        for comp in competitors:
            # Get latest alert summary
            alert_res = await db.execute(select(Alert).where(Alert.competitor_id == comp.id).order_by(Alert.created_at.desc()).limit(1))
            latest_alert = alert_res.scalar_one_or_none()
            
            # Get latest prediction
            pred_res = await db.execute(select(Prediction).where(Prediction.competitor_id == comp.id).order_by(Prediction.created_at.desc()).limit(1))
            latest_pred = pred_res.scalar_one_or_none()
            
            report_competitors.append({
                "name": comp.name,
                "summary": latest_alert.description if latest_alert else "No recent changes detected.",
                "threat_score": 90 if (latest_alert and latest_alert.severity == "RED") else (50 if latest_alert and latest_alert.severity == "YELLOW" else 10),
                "predicted_action": latest_pred.content if latest_pred else "Not enough data for a prediction."
            })
            
        report_data = {"competitors": report_competitors}
        
        # Email target
        import os
        target_email = os.getenv("SMTP_USER", "vishnus202004@gmail.com")
        await send_intel_report([target_email], report_data)
        logger.info(f"Weekly digest dispatched to {target_email}")


def start_scheduler():
    """Starts the APScheduler background job. Called once on FastAPI startup."""
    logger.info("Starting APScheduler — Intelligence cycle runs every 6 hours, Digest weekly.")
    
    # 6-hour scrape job
    scheduler.add_job(
        automated_intelligence_job,
        trigger="interval",
        hours=6,
        id="intelligence_cycle",
        replace_existing=True
    )
    
    # Weekly digest email (Every Monday at 8 AM)
    scheduler.add_job(
        automated_weekly_report_job,
        trigger="cron",
        day_of_week="mon",
        hour=8,
        minute=0,
        id="weekly_digest",
        replace_existing=True
    )
    
    scheduler.start()

