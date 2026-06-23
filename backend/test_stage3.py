import asyncio
import logging
import sys

from app.services.vector_store import store_scraped_content, store_news_article, vector_store

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_stage3")


async def test_vector_store():
    logger.info("Initializing Test Stage 3: Vector Store and Embeddings...")

    # 1. Test storing scraped content
    sample_scraped_content = """
    IntelGraphX Competitor 
    We just launched our new Enterprise Tier pricing! It now starts at $49 per user/month and includes advanced Single Sign-On (SSO), granular access controls, and custom integrations.
    Our basic plan is still free forever for teams up to 5 people.
    """
    
    logger.info("Storing sample website content...")
    await store_scraped_content(
        competitor_id=101,
        url="https://example-competitor.com/pricing",
        content=sample_scraped_content
    )

    # 2. Test storing a news article
    sample_news_article = {
        "title": "Example Competitor acquires AI startup",
        "description": "In a surprise move, Example Competitor announced today the acquisition of Brain AI, an artificial intelligence startup focusing on workflow automation, for $150M in cash.",
        "url": "https://news.example.com/acquisition",
        "source": "TechCrunch",
        "published_at": "2026-06-20T14:00:00Z"
    }

    logger.info("Storing sample news article...")
    await store_news_article(
        competitor_name="Example Competitor",
        article=sample_news_article
    )

    # 3. Test Retrieval / Semantic Search
    logger.info("Testing semantic retrieval with a search query...")
    
    query1 = "How much does the enterprise plan cost?"
    logger.info(f"Query 1: '{query1}'")
    results1 = vector_store.similarity_search(query1, k=1)
    for res in results1:
        logger.info(f"Retrieved Result: {res.page_content[:200].strip()}")
        logger.info(f"Metadata: {res.metadata}")

    query2 = "Which company was acquired for 150 million?"
    logger.info(f"Query 2: '{query2}'")
    results2 = vector_store.similarity_search(query2, k=1)
    for res in results2:
        logger.info(f"Retrieved Result: {res.page_content[:200].strip()}")
        logger.info(f"Metadata: {res.metadata}")

    logger.info("Test Stage 3 Completed Successfully.")

if __name__ == "__main__":
    asyncio.run(test_vector_store())
