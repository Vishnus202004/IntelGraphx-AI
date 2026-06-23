import hashlib
import logging
from datetime import datetime
from playwright.async_api import async_playwright
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.hash import Hash

logger = logging.getLogger(__name__)


async def scrape_url(url: str) -> str:
    """
    Scrapes the text content of a web page using headless Playwright.
    Bypasses simple scraper blockers by setting common headers and a standard User-Agent.
    """
    logger.info(f"Starting web scrape for URL: {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                ignore_https_errors=True
            )
            page = await context.new_page()
            
  
            response = await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            if not response:
                raise ValueError(f"Failed to receive response from {url}")
            
            if response.status >= 400:
                logger.warning(f"Received HTTP {response.status} from {url}. Continuing anyway, but content may be restricted.")
               

            await page.wait_for_timeout(3000)


            body_text = await page.evaluate("() => document.body.innerText")
            
         
            lines = [line.strip() for line in body_text.split("\n") if line.strip()]
            cleaned_text = "\n".join(lines)
            
            logger.info(f"Successfully scraped {len(cleaned_text)} characters from {url}")
            return cleaned_text
        except Exception as e:
            logger.error(f"Error occurred while scraping {url}: {str(e)}")
            return f"Scraping failed or blocked by anti-bot protection. Error: {str(e)}"
        finally:
            await browser.close()


def compute_sha256(text: str) -> str:
    """
    Utility to compute SHA-256 hash of a string.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


async def detect_webpage_changes(db: AsyncSession, competitor_id: int, url: str) -> dict:
    """
    Scrapes a URL, computes its hash, compares it with the stored hash for this competitor URL,
    and updates the database if it has changed.
    """

    scraped_content = await scrape_url(url)
    current_hash = compute_sha256(scraped_content)

  
    stmt = select(Hash).filter(Hash.competitor_id == competitor_id, Hash.url == url)
    result = await db.execute(stmt)
    db_hash_record = result.scalars().first()

    has_changed = False
    old_hash = None

    if db_hash_record is None:
       
        has_changed = True
        new_record = Hash(
            competitor_id=competitor_id,
            url=url,
            content_hash=current_hash,
            checked_at=datetime.utcnow()
        )
        db.add(new_record)
        await db.commit()
        logger.info(f"No existing hash found for competitor {competitor_id} URL {url}. Created record.")
    else:
        old_hash = db_hash_record.content_hash
        if old_hash != current_hash:
            has_changed = True
            db_hash_record.content_hash = current_hash
            db_hash_record.checked_at = datetime.utcnow()
            await db.commit()
            logger.info(f"Change detected for competitor {competitor_id} URL {url}. Updated hash record.")
        else:
            db_hash_record.checked_at = datetime.utcnow()
            await db.commit()
            logger.info(f"No changes detected for competitor {competitor_id} URL {url}.")

    return {
        "competitor_id": competitor_id,
        "url": url,
        "has_changed": has_changed,
        "old_hash": old_hash,
        "new_hash": current_hash,
        "content": scraped_content
    }
