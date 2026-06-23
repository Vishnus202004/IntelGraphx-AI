import logging
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from sqlalchemy.future import select

from app.core.config import settings
from app.core.database import async_session_maker
from app.agents.state import AgentState
from app.models.alert import Alert
from app.models.prediction import Prediction

logger = logging.getLogger(__name__)

if settings.GROQ_API_KEY:
    llm = ChatGroq(
        temperature=0.2,
        model_name="llama-3.1-8b-instant",
        api_key=settings.GROQ_API_KEY
    )
else:
    llm = None


async def pattern_node(state: AgentState) -> dict:
    """
    Analyzes historical data (alerts and predictions) to find recurring cycles
    before passing to the Forecast agent.
    """
    logger.info(f"Node: Pattern for competitor {state['competitor_name']}")

    if not llm:
        return {
            "identified_patterns": "Pattern analysis skipped. LLM not configured.",
            "messages": []
        }


    historical_alerts = []
    historical_preds = []
    
    try:
        async with async_session_maker() as db:
 
            alert_res = await db.execute(
                select(Alert).where(Alert.competitor_id == state.get("competitor_id", 0))
                .order_by(Alert.created_at.desc()).limit(10)
            )
            historical_alerts = alert_res.scalars().all()


            pred_res = await db.execute(
                select(Prediction).where(Prediction.competitor_id == state.get("competitor_id", 0))
                .order_by(Prediction.created_at.desc()).limit(5)
            )
            historical_preds = pred_res.scalars().all()
    except Exception as e:
        logger.error(f"Failed to retrieve history for pattern analysis: {e}")


    alerts_text = "\n".join([f"- {a.created_at.date()}: [{a.severity}] {a.title} - {a.description}" for a in historical_alerts]) or "No historical alerts."
    preds_text = "\n".join([f"- {p.created_at.date()}: (Conf: {p.confidence}) {p.content}" for p in historical_preds]) or "No historical predictions."

    system_prompt = """You are a strategic Pattern Recognition AI specialized in competitor intelligence.
Analyze the historical alerts, predictions, and current analysis. 
Identify any recurring cycles or patterns (e.g., "Price increase every 150 days", "Feature launches typically follow marketing pushes").
If there are no clear patterns, state that explicitly.
Keep your response concise and focused only on the detected patterns."""

    user_content = f"""
Competitor: {state.get('competitor_name')}

--- Current Analysis Summary ---
{state.get('analysis_summary', 'No analysis available.')}

--- Historical Alerts (Last 10) ---
{alerts_text}

--- Historical Predictions (Last 5) ---
{preds_text}

Identify the key strategic patterns or recurring cycles for this competitor.
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ]

    try:
        response = await llm.ainvoke(messages)
        identified_patterns = response.content.strip()
        logger.info(f"Identified patterns: {identified_patterns[:100]}...")
        
        return {
            "identified_patterns": identified_patterns,
            "messages": [response]
        }
    except Exception as e:
        logger.error(f"Failed to run Pattern Node: {str(e)}")
        return {
            "identified_patterns": "Error during pattern generation.",
            "messages": []
        }
