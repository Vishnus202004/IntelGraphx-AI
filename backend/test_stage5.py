import asyncio
import logging
import sys

from app.agents.graph import agent_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_stage5")

async def test_langgraph_hitl():
    logger.info("Initializing Test Stage 5: Forecasting & Human-in-the-Loop...")
    
    # LangGraph requires a thread configuration to track state when using MemorySaver
    config = {"configurable": {"thread_id": "competitor-101-thread-1"}}
    
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
        "predicted_action": "",
        "confidence_score": 0.0,
        "alert_severity": "",
        "alert_title": "",
        "messages": []
    }
    
    logger.info("Starting pipeline. It should pause before the 'alert' node.")
    try:
        # Run the graph until it hits the interrupt_before hook
        async for event in agent_pipeline.astream(initial_state, config=config, stream_mode="values"):
            pass
            
        logger.info("--- Pipeline Paused (Human-in-the-Loop) ---")
        
        # Check current state from Memory Checkpointer
        state_snapshot = agent_pipeline.get_state(config)
        paused_state = state_snapshot.values
        next_nodes = state_snapshot.next
        
        logger.info(f"Pending Nodes to execute next: {next_nodes}")
        logger.info(f"Threat Score Computed: {paused_state.get('threat_score')}")
        logger.info(f"Predicted Action: {paused_state.get('predicted_action')}")
        logger.info(f"Confidence Score: {paused_state.get('confidence_score')}")
        
        # Simulate Human Approval
        if "alert" in next_nodes:
            logger.info("\n[HUMAN APPROVAL GRANTED] Resuming graph execution to generate alert...\n")
            
            # Resume graph with None input to continue from checkpoint
            async for event in agent_pipeline.astream(None, config=config, stream_mode="values"):
                pass
                
            final_snapshot = agent_pipeline.get_state(config)
            final_state = final_snapshot.values
            
            logger.info("--- Pipeline Completed ---")
            logger.info(f"Alert Generated: {final_state.get('alert_title')} (Severity: {final_state.get('alert_severity')})")
        else:
            logger.warning("Pipeline did not pause at 'alert' node as expected.")
            
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(test_langgraph_hitl())
