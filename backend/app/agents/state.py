import operator
from typing import TypedDict, List, Dict, Any, Annotated

class AgentState(TypedDict):

    competitor_id: int
    competitor_name: str
    url: str
    

    has_changed: bool
    scraped_content: str
    recent_news: List[Dict[str, Any]]
    

    relevant_chunks: List[str]
    

    analysis_summary: str
    threat_score: int
    recommendation: str
    

    reflection_feedback: str
    analysis_attempts: int
    is_analysis_valid: bool
    

    identified_patterns: str
    

    alert_severity: str
    alert_title: str
    

    predicted_action: str
    confidence_score: float
    

    messages: Annotated[List[Any], operator.add]
