import asyncio
import logging
import sys
from sqlalchemy.future import select

from app.core.database import async_session_maker
from app.models.competitor import Competitor
from app.services.scraper import detect_webpage_changes
from app.services.news import get_competitor_news

# Set up logging to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("test_stage2")


async def test_scraper_and_news():
    logger.info("Initializing Test Stage 2: Scraper and News Integration...")
    
    async with async_session_maker() as session:
        # 1. Fetch competitors
        logger.info("Fetching competitors from database...")
        stmt = select(Competitor).filter(Competitor.is_active == True)
        result = await session.execute(stmt)
        competitors = result.scalars().all()
        
        if not competitors:
            logger.error("No competitors found in the database. Please run init_db.py first.")
            return

        # We will test using ClickUp
        target_competitor = None
        for comp in competitors:
            if comp.name == "ClickUp":
                target_competitor = comp
                break
        
        if not target_competitor:
            target_competitor = competitors[0]

        logger.info(f"Selected competitor for live test: {target_competitor.name}")
        
        # 2. Run Scraper with change detection on the pricing URL
        # Let's verify we have a pricing URL
        pricing_url = target_competitor.pricing_url or "https://clickup.com/pricing"
        logger.info(f"Testing Scraper on URL: {pricing_url}")
        
        try:
            scrape_result = await detect_webpage_changes(
                db=session,
                competitor_id=target_competitor.id,
                url=pricing_url
            )
            
            logger.info("--- Scrape Result Summary ---")
            logger.info(f"Competitor ID: {scrape_result['competitor_id']}")
            logger.info(f"URL: {scrape_result['url']}")
            logger.info(f"Has Changed: {scrape_result['has_changed']}")
            logger.info(f"Old Hash: {scrape_result['old_hash']}")
            logger.info(f"New Hash: {scrape_result['new_hash']}")
            logger.info(f"Content Length (characters): {len(scrape_result['content'])}")
            logger.info(f"First 300 characters of scraped content:\n{scrape_result['content'][:300]}")
            
        except Exception as e:
            logger.error(f"Scraper test failed: {str(e)}", exc_info=True)

        # 3. Run News Monitor to fetch real news
        logger.info(f"Testing News Fetcher for competitor name: {target_competitor.name}")
        try:
            news_articles = await get_competitor_news(target_competitor.name)
            logger.info(f"Found {len(news_articles)} news articles.")
            
            for idx, article in enumerate(news_articles[:3]):
                logger.info(f"--- Article #{idx+1} ---")
                logger.info(f"Title: {article['title']}")
                logger.info(f"Source: {article['source']}")
                logger.info(f"Published At: {article['published_at']}")
                logger.info(f"URL: {article['url']}")
                logger.info(f"Snippet: {article['description'][:150]}...")
                
        except Exception as e:
            logger.error(f"News fetcher test failed: {str(e)}", exc_info=True)

    logger.info("Test Stage 2 Completed.")

if __name__ == "__main__":
    asyncio.run(test_scraper_and_news())
