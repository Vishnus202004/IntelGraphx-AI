import json
import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# RAGAS-equivalent evaluation using LLM-as-Judge with Groq
# Computes Faithfulness, Answer Relevancy, and Context Relevance scores
# ---------------------------------------------------------------------------

EVAL_PROMPT = ChatPromptTemplate.from_template("""
You are an expert evaluator assessing the quality of an AI-generated intelligence analysis.

## Context (retrieved from competitor data):
{context}

## Question asked:
{question}

## AI-generated analysis:
{analysis}

Score the following three RAGAS-equivalent metrics on a scale of 0.0 to 1.0:

1. **Faithfulness** – Is every claim in the analysis grounded in the provided context?
   (1.0 = fully grounded, 0.0 = hallucinated or contradicts context)

2. **Answer Relevancy** – Does the analysis directly answer the question asked?
   (1.0 = fully on-topic, 0.0 = irrelevant)

3. **Context Relevance** – Is the retrieved context relevant to answering the question?
   (1.0 = highly relevant, 0.0 = unrelated context)

Respond ONLY with valid JSON in this exact format, no extra text:
{{"faithfulness": 0.0, "answer_relevancy": 0.0, "context_relevance": 0.0}}
""")


def evaluation_node(state: dict):
    """
    RAGAS-equivalent evaluation node.
    Scores the AI pipeline output using LLM-as-Judge with Faithfulness,
    Answer Relevancy, and Context Relevance metrics (inspired by RAGAS).
    """
    logger.info("--- EVALUATION AGENT RUNNING (RAGAS-equivalent LLM-as-Judge) ---")

    context_chunk = str(state.get("scraped_content", ""))[:3000]
    analysis = state.get("analysis_summary", "")
    competitor_name = state.get("competitor_name", "this competitor")
    question = f"What are the recent strategic changes and threats from {competitor_name}?"

    if not context_chunk or not analysis:
        logger.warning("Missing context or analysis. Skipping evaluation.")
        return state

    try:
        llm = ChatGroq(
            temperature=0,
            model_name="llama-3.1-8b-instant",
            groq_api_key=settings.GROQ_API_KEY
        )

        chain = EVAL_PROMPT | llm
        response = chain.invoke({
            "context": context_chunk,
            "question": question,
            "analysis": analysis
        })

        # Parse JSON scores from LLM response
        raw = response.content.strip()
        # Extract JSON even if surrounded by markdown fences
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()

        scores = json.loads(raw)

        faithfulness = float(scores.get("faithfulness", 0.0))
        answer_relevancy = float(scores.get("answer_relevancy", 0.0))
        context_relevance = float(scores.get("context_relevance", 0.0))

        logger.info(
            f"RAGAS Evaluation Metrics — "
            f"Faithfulness: {faithfulness:.2f} | "
            f"Answer Relevancy: {answer_relevancy:.2f} | "
            f"Context Relevance: {context_relevance:.2f}"
        )

        state["evaluation_metrics"] = {
            "faithfulness": faithfulness,
            "answer_relevancy": answer_relevancy,
            "context_relevance": context_relevance
        }

    except Exception as e:
        logger.error(f"RAGAS Evaluation Agent failed: {e}", exc_info=True)

    return state
