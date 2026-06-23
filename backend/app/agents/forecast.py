import json
import asyncio
import logging
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from app.core.config import settings
from app.core.database import async_session_maker
from app.agents.state import AgentState
from app.models.prediction import Prediction

logger = logging.getLogger(__name__)

if settings.GROQ_API_KEY:
    llm = ChatGroq(
        temperature=0.6,
        model_name="llama-3.1-8b-instant",
        api_key=settings.GROQ_API_KEY
    )
else:
    llm = None


async def forecast_node(state: AgentState) -> dict:
    """
    Predicts the next strategic move of the competitor using Groq and
    PERSISTS the Prediction record to the SQLite database asynchronously.
    """
    logger.info(f"Node: Forecast for competitor {state['competitor_name']}")

    if not llm:
        return {
            "predicted_action": "Unable to predict. LLM not configured.",
            "confidence_score": 0.0,
            "messages": []
        }

    system_prompt = """You are a predictive analytics engine specialising in SaaS competitor intelligence.
Based on the competitor's recent actions and analysis, predict their next logical strategic move.

Assess your confidence score dynamically based on the completeness and certainty of the evidence:
- Assign 0.90+ only if there is definitive, explicit proof of an upcoming action.
- Assign 0.70 - 0.89 if there are strong indicators or consistent historical trends.
- Assign 0.40 - 0.69 if the prediction is speculative or based on weak/noisy signals.
Be precise and avoid clustering your confidence scores around common default values like 0.85.

Respond STRICTLY in JSON format with exactly two keys:
{
  "predicted_action": "A clear, concise sentence predicting their next move.",
  "confidence_score": <float between 0.0 and 1.0 representing your confidence score>
}"""

    user_content = f"""
Competitor: {state.get('competitor_name')}

--- Analysis Summary ---
{state.get('analysis_summary', 'No analysis available.')}

--- Identified Patterns ---
{state.get('identified_patterns', 'No historical patterns identified.')}

--- Recommendation ---
{state.get('recommendation', '')}

What is their next most likely strategic move?
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
        predicted_action = data.get("predicted_action", "No prediction generated.")
        confidence_score = float(data.get("confidence_score", 0.0))

        # Persist to database natively
        title = f"Forecast: {state['competitor_name']}"
        async with async_session_maker() as db:
            pred = Prediction(
                competitor_id=state.get("competitor_id", 0),
                title=title,
                content=predicted_action[:1024],
                confidence=round(confidence_score, 4),
            )
            db.add(pred)
            await db.commit()
            logger.info(f"Persisted Prediction to DB for competitor_id={pred.competitor_id}")

        return {
            "predicted_action": predicted_action,
            "confidence_score": confidence_score,
            "messages": [response]
        }
    except Exception as e:
        logger.error(f"Failed to parse Forecast JSON: {content} | Error: {str(e)}")
        return {
            "predicted_action": "Error generating prediction.",
            "confidence_score": 0.0,
            "messages": [response]
        }
