import logging
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Optional
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


async def fetch_news_via_newsapi(query: str, api_key: str) -> List[Dict]:
    """
    Fetches news articles from NewsAPI for a given search query.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": api_key
    }
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])
                results = []
                for art in articles:
                    results.append({
                        "title": art.get("title"),
                        "description": art.get("description") or art.get("content") or "",
                        "url": art.get("url"),
                        "source": art.get("source", {}).get("name", "NewsAPI"),
                        "published_at": art.get("publishedAt")
                    })
                return results
            else:
                logger.error(f"NewsAPI error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"Failed to query NewsAPI: {str(e)}")
            return []


async def fetch_news_via_google_rss(query: str) -> List[Dict]:
    """
    Fetches real-time news articles from Google News RSS feed for a given query.
    Requires no API keys, enabling fully live data extraction in local environments.
    """
    # RSS url-escaped search
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}"
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code != 200:
                logger.error(f"Google RSS error: {response.status_code}")
                return []
            
            # Parse XML
            root = ET.fromstring(response.content)
            channel = root.find("channel")
            if channel is None:
                return []
            
            items = channel.findall("item")
            results = []
            
            # Extract top 10 articles
            for item in items[:10]:
                title = item.findtext("title")
                link = item.findtext("link")
                pub_date_str = item.findtext("pubDate")
                source = item.find("source")
                source_name = source.text if source is not None else "Google News RSS"
                description = item.findtext("description")
                
                # Convert publication date from RFC 822 format (e.g. 'Mon, 22 Jun 2026 12:00:00 GMT')
                # to ISO string. Default to current time if parsing fails.
                published_at = datetime.utcnow().isoformat() + "Z"
                if pub_date_str:
                    try:
                        # Attempt standard RFC 822 parse
                        dt = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
                        published_at = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                    except Exception:
                        pass
                
                results.append({
                    "title": title,
                    "description": description or "",
                    "url": link,
                    "source": source_name,
                    "published_at": published_at
                })
                
            return results
        except Exception as e:
            logger.error(f"Failed to query Google RSS news for query '{query}': {str(e)}")
            return []


async def get_competitor_news(competitor_name: str) -> List[Dict]:
    """
    Retrieves real live news for a competitor.
    Uses NewsAPI if a key is provided, otherwise falls back to Google News RSS search.
    """
    logger.info(f"Retrieving news for competitor: {competitor_name}")
    api_key = settings.NEWS_API_KEY
    
    if api_key and api_key.strip():
        logger.info("Using NewsAPI for fetching articles.")
        results = await fetch_news_via_newsapi(competitor_name, api_key)
        if results:
            return results
        logger.info("NewsAPI returned 0 results. Trying Google RSS fallback.")
        
    logger.info("Using Google News RSS query.")
    return await fetch_news_via_google_rss(competitor_name)
