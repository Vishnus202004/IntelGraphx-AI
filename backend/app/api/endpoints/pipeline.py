from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.competitor import Competitor
from app.services.scraper import detect_webpage_changes
from app.services.news import fetch_news_via_google_rss
from app.services.vector_store import store_scraped_content
from app.agents.graph import agent_pipeline

router = APIRouter()

# In-memory tracker for currently running pipelines
active_pipelines = set()

async def _run_pipeline_for(competitor_id: int):
    active_pipelines.add(competitor_id)
    """Runs the full intelligence pipeline for a single competitor."""

    from app.core.database import async_session_maker

    async with async_session_maker() as db:
        result = await db.execute(select(Competitor).where(Competitor.id == competitor_id))
        comp = result.scalar_one_or_none()
        if not comp:
            return

        try:
            # 1. Scrape
            scrape_result = await detect_webpage_changes(db=db, competitor_id=comp.id, url=comp.domain)
            scraped_text = scrape_result.get("content", "Failed to scrape content.")
            has_changed = scrape_result.get("has_changed", False)

            # 2. Embed into ChromaDB
            await store_scraped_content(competitor_id=comp.id, url=comp.domain, content=scraped_text)

            # 3. Fetch news
            news_items = await fetch_news_via_google_rss(comp.name)

            # 4. Run LangGraph pipeline
            config = {"configurable": {"thread_id": f"comp-{comp.id}-manual"}}
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

            await agent_pipeline.ainvoke(initial_state, config=config)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Manual pipeline failed for {comp.name}: {str(e)}", exc_info=True)
        finally:
            active_pipelines.discard(competitor_id)

@router.get("/status")
async def get_pipeline_status():
    """Returns the list of competitor IDs that are currently running."""
    return {"active_pipelines": list(active_pipelines)}



@router.post("/{competitor_id}/run")
async def trigger_pipeline(
    competitor_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger the full intelligence pipeline for a competitor.
    Runs scraping, ChromaDB embedding, Groq analysis, and forecasting
    in the background so the response returns immediately.
    """
    result = await db.execute(select(Competitor).where(Competitor.id == competitor_id))
    comp = result.scalar_one_or_none()
    if not comp:
        raise HTTPException(status_code=404, detail="Competitor not found")

    background_tasks.add_task(_run_pipeline_for, competitor_id)

    return {
        "message": f"Intelligence pipeline triggered for {comp.name}. Results will appear on the Dashboard shortly."
    }

@router.post("/{competitor_id}/resume")
async def resume_pipeline(competitor_id: int, background_tasks: BackgroundTasks):
    """
    Resume a paused Human-in-the-Loop pipeline for a specific competitor.
    """
    async def _resume_task():
        try:
            config = {"configurable": {"thread_id": f"comp-{competitor_id}-manual"}}
            await agent_pipeline.ainvoke(None, config=config)
            
            # Also try the scheduler thread id just in case it was paused there
            config_sched = {"configurable": {"thread_id": f"comp-{competitor_id}-scheduler"}}
            await agent_pipeline.ainvoke(None, config=config_sched)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Resume failed: {e}")

    background_tasks.add_task(_resume_task)
    return {"message": "Pipeline resumption triggered."}
