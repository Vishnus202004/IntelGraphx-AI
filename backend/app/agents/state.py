import operator
from typing import TypedDict, List, Dict, Any, Annotated

class AgentState(TypedDict):
    # Input Context
    competitor_id: int
    competitor_name: str
    url: str
    
    # Raw Data
    has_changed: bool
    scraped_content: str
    recent_news: List[Dict[str, Any]]
    
    # RAG Retrieval Context
    relevant_chunks: List[str]
    
    # Analysis Output
    analysis_summary: str
    threat_score: int
    recommendation: str
    
    # Reflection & Validation Loop
    reflection_feedback: str
    analysis_attempts: int
    is_analysis_valid: bool
    
    # Pattern Recognition
    identified_patterns: str
    
    # Alert Generation
    alert_severity: str
    alert_title: str
    
    # Forecasting
    predicted_action: str
    confidence_score: float
    
    # Standard LangGraph message history appending
    messages: Annotated[List[Any], operator.add]
