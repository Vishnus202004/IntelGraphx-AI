import json
import asyncio
import logging
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import async_session_maker
from app.agents.state import AgentState
from app.services.vector_store import vector_store
from app.models.alert import Alert

logger = logging.getLogger(__name__)


if settings.GROQ_API_KEY:
    llm = ChatGroq(
        temperature=0.2,
        model_name="llama-3.1-8b-instant",
        api_key=settings.GROQ_API_KEY
    )
else:
    logger.warning("GROQ_API_KEY not found. Analysis agent will fail without an LLM.")
    llm = None


def retrieval_node(state: AgentState) -> dict:
    """
    Retrieves historical context about the competitor from ChromaDB.
    """
    logger.info(f"Node: Retrieval for competitor {state['competitor_name']}")
    query = f"Recent changes, pricing, and news regarding {state['competitor_name']}"
    docs = vector_store.similarity_search(query, k=3)
    relevant_chunks = [doc.page_content for doc in docs]
    return {"relevant_chunks": relevant_chunks}


async def analysis_node(state: AgentState) -> dict:
    """
    Uses Groq LLM to analyze competitor data and generate intelligence JSON.
    """
    logger.info("Node: Analysis")

    system_prompt = """You are a top-tier Competitor Intelligence Analyst.
You will be provided with scraped website content, recent news, and historical vector search context.
Analyze the competitor's actions. Determine if there are pricing changes, new feature launches, or strategic shifts.

Respond STRICTLY in JSON format with exactly three keys:
{
  "summary": "Detailed summary of the changes.",
  "threat_score": <integer between 0 and 100>,
  "recommendation": "Strategic recommendation for our product team."
}"""

    user_content = f"""
Competitor: {state.get('competitor_name')}

--- Scraped Website Updates ---
{state.get('scraped_content', 'No website content available.')[:1500]}

--- Recent News ---
{str([{'title': n.get('title'), 'desc': n.get('description')[:200]} for n in state.get('recent_news', [])[:3]])}

--- Historical Context (Vector Store) ---
{state.get('relevant_chunks', [])}

--- Reflection Feedback (If retrying) ---
{state.get('reflection_feedback', 'None. This is the first attempt.')}
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ]

    response = await llm.ainvoke(messages)
    content = response.content.strip()

    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()

    try:
        data = json.loads(content)
        return {
            "analysis_summary": data.get("summary", ""),
            "threat_score": int(data.get("threat_score", 0)),
            "recommendation": data.get("recommendation", ""),
            "analysis_attempts": state.get("analysis_attempts", 0) + 1,
            "messages": [response]
        }
    except Exception as e:
        logger.error(f"Failed to parse JSON response: {content} | Error: {str(e)}")
        return {
            "analysis_summary": "Error parsing analysis.",
            "threat_score": 0,
            "recommendation": "Check LLM output.",
            "analysis_attempts": state.get("analysis_attempts", 0) + 1,
            "messages": [response]
        }


def reflection_node(state: AgentState) -> dict:
    """
    Reflects on the analysis to ensure it meets quality standards.
    """
    logger.info("Node: Reflection")
    summary = state.get("analysis_summary", "")
    attempts = state.get("analysis_attempts", 0)

    if attempts >= 3:
        logger.info("Max analysis attempts reached. Forcing valid state.")
        return {"is_analysis_valid": True, "reflection_feedback": "Max retries reached."}

    if len(summary) < 50:
        return {"is_analysis_valid": False, "reflection_feedback": "The summary is too brief. Provide a more detailed analysis."}

    if "error parsing" in summary.lower():
        return {"is_analysis_valid": False, "reflection_feedback": "Output was not valid JSON. Ensure strict JSON compliance."}

    return {"is_analysis_valid": True, "reflection_feedback": "Analysis looks solid."}


async def alert_node(state: AgentState) -> dict:
    """
    Determines alert severity based on the final threat score and
    PERSISTS the alert record to the SQLite database asynchronously.
    """
    logger.info("Node: Alert Generation")
    score = state.get("threat_score", 0)

    severity = "GREEN"
    if score >= 80:
        severity = "RED"
    elif score >= 50:
        severity = "YELLOW"

    title = f"[{severity}] Intel Update: {state['competitor_name']} Action Detected"


    async with async_session_maker() as db:
        alert = Alert(
            competitor_id=state.get("competitor_id", 0),
            severity=severity,
            title=title,
            description=state.get("analysis_summary", "No summary available.")[:1024],
            is_approved=False,
        )
        db.add(alert)
        await db.commit()
        logger.info(f"Persisted Alert [{severity}] to database for competitor_id={alert.competitor_id}")

    return {
        "alert_severity": severity,
        "alert_title": title
    }
