from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.vector_store import get_vector_store
from app.core.database import get_db
from app.models.competitor import Competitor
from app.models.alert import Alert
from app.models.prediction import Prediction
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    deep_mode: bool = False

class ChatResponse(BaseModel):
    response: str


@router.post("/", response_model=ChatResponse)
async def chat_with_analyst(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Conversational RAG endpoint that:
      1. Fetches the current competitor list from SQLite
      2. Fetches recent alerts and predictions from SQLite
      3. Retrieves related chunks from ChromaDB
      4. Sends everything to Groq Llama 3.1 for a grounded answer
    """
    try:
        # ------ Live DB context ------
        comp_result = await db.execute(select(Competitor))
        comps = comp_result.scalars().all()
        comp_lines = "\n".join(
            [f"- {c.name} (domain: {c.domain}, pricing: {c.pricing_url or 'N/A'})" for c in comps]
        ) or "No competitors are currently being tracked."

        alert_result = await db.execute(
            select(Alert).order_by(Alert.created_at.desc()).limit(5)
        )
        recent_alerts = alert_result.scalars().all()
        alert_lines = "\n".join(
            [f"- [{a.severity}] {a.title}: {a.description[:200]}" for a in recent_alerts]
        ) or "No alerts generated yet."

        pred_result = await db.execute(
            select(Prediction).order_by(Prediction.created_at.desc()).limit(5)
        )
        recent_preds = pred_result.scalars().all()
        pred_lines = "\n".join(
            [f"- {p.title} ({round(p.confidence*100)}% confidence): {p.content[:200]}" for p in recent_preds]
        ) or "No predictions generated yet."

        # ------ ChromaDB RAG context ------
        vector_store = get_vector_store()
        docs = vector_store.similarity_search(request.message, k=5)
        rag_context = "\n\n".join([f"Source: {d.metadata.get('url', 'Unknown')} - {d.page_content}" for d in docs]) if docs else "No vector data available yet."

        # ------ Build full context ------
        full_context = f"""=== Currently Tracked Competitors ===
{comp_lines}

=== Recent Intelligence Alerts ===
{alert_lines}

=== Recent AI Predictions ===
{pred_lines}

=== Vector Store Knowledge (RAG) ===
{rag_context}"""

        # ------ LLM Generation ------
        llm = ChatGroq(
            temperature=0.3,
            model_name="llama-3.1-8b-instant",
            groq_api_key=settings.GROQ_API_KEY
        )

        sys_prompt = "You are the IntelGraphX AI Analyst. Answer the user's strategic questions about competitors using the provided context below. Be concise, insightful, and professional. Always reference specific competitors by name when available. If the context lacks detail, say so honestly."
        if request.deep_mode:
            sys_prompt += " Since Deep Analysis Mode is enabled, you MUST append a 'Sources Cited' section at the end of your response, listing the exact Source URLs used from the Vector Store Knowledge."

        prompt = ChatPromptTemplate.from_messages([
            ("system", f"{sys_prompt}\n\nContext:\n{{context}}"),
            ("human", "{question}")
        ])

        chain = prompt | llm
        result = chain.invoke({"context": full_context, "question": request.message})

        return ChatResponse(response=result.content)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI response: {str(e)}"
        )
