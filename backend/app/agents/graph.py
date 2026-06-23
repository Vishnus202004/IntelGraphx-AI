from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.agents.state import AgentState
from app.agents.nodes import retrieval_node, analysis_node, reflection_node, alert_node
from app.agents.forecast import forecast_node
from app.agents.evaluator import evaluation_node
from app.agents.pattern import pattern_node

def should_continue(state: AgentState):
    """
    Conditional edge function that routes back to Analysis if the Reflection 
    determined the output was invalid, or proceeds to Pattern if valid.
    """
    if state.get("is_analysis_valid", False):
        return "pattern"
    return "analysis"

# Initialize graph
workflow = StateGraph(AgentState)

# Add all nodes
workflow.add_node("retrieval", retrieval_node)
workflow.add_node("analysis", analysis_node)
workflow.add_node("reflection", reflection_node)
workflow.add_node("pattern", pattern_node)
workflow.add_node("forecast", forecast_node)
workflow.add_node("alert", alert_node)
workflow.add_node("evaluation", evaluation_node)

# Add standard edges
workflow.add_edge(START, "retrieval")
workflow.add_edge("retrieval", "analysis")
workflow.add_edge("analysis", "reflection")

# Conditional reflection loop: retry analysis or proceed to pattern
workflow.add_conditional_edges(
    "reflection",
    should_continue,
    {
        "analysis": "analysis",
        "pattern": "pattern"
    }
)

# Post-reflection linear pipeline
workflow.add_edge("pattern", "forecast")
workflow.add_edge("forecast", "alert")
workflow.add_edge("alert", "evaluation")
workflow.add_edge("evaluation", END)

# Initialize memory checkpointer for Human-in-the-Loop execution
memory = MemorySaver()

# Compile the graph into an executable agent pipeline
# interrupt_before=["alert"] enables true Human-in-the-Loop pause
agent_pipeline = workflow.compile(
    checkpointer=memory,
    interrupt_before=["alert"]
)
