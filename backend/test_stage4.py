import asyncio
import logging
import sys

from app.agents.graph import agent_pipeline
from app.agents.state import AgentState

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_stage4")

async def test_langgraph():
    logger.info("Initializing Test Stage 4: LangGraph Multi-Agent Flow...")
    
    # Define an initial mock state to pass into the graph
    initial_state = {
        "competitor_id": 101,
        "competitor_name": "Example Competitor",
        "url": "https://example-competitor.com",
        "has_changed": True,
        "scraped_content": "We just raised our Enterprise tier by 20% to $60 per user/month.",
        "recent_news": [
            {"title": "Example Competitor raises prices", "description": "Prices are up 20%"}
        ],
        "relevant_chunks": [],
        "analysis_summary": "",
        "threat_score": 0,
        "recommendation": "",
        "reflection_feedback": "",
        "analysis_attempts": 0,
        "is_analysis_valid": False,
        "alert_severity": "",
        "alert_title": "",
        "messages": []
    }
    
    logger.info("Invoking LangGraph pipeline. This will contact Groq API...")
    try:
        final_state = await agent_pipeline.ainvoke(initial_state)
        
        logger.info("--- LangGraph Execution Complete ---")
        logger.info(f"Final Threat Score: {final_state.get('threat_score')}")
        logger.info(f"Analysis Summary:\n{final_state.get('analysis_summary')}")
        logger.info(f"Recommendation:\n{final_state.get('recommendation')}")
        logger.info(f"Alert Generated: {final_state.get('alert_title')} (Severity: {final_state.get('alert_severity')})")
        logger.info(f"Total Analysis Attempts (Reflection Loops): {final_state.get('analysis_attempts')}")
        
    except Exception as e:
        logger.error(f"LangGraph execution failed: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(test_langgraph())
