import logging
from typing import List, Dict, Any
from datetime import datetime

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

logger = logging.getLogger(__name__)

# Initialize local embedding model for completely free and private offline embeddings
try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
except Exception as e:
    logger.error(f"Failed to load HuggingFace Embeddings: {str(e)}")
    raise e

# Initialize ChromaDB persistent vector store
CHROMA_PERSIST_DIR = "./chroma_db"

vector_store = Chroma(
    collection_name="intelgraphx_knowledge",
    embedding_function=embeddings,
    persist_directory=CHROMA_PERSIST_DIR
)

# Initialize text chunker
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)


async def store_scraped_content(competitor_id: int, url: str, content: str) -> None:
    """
    Chunks and stores the text content of a scraped web page into ChromaDB.
    """
    logger.info(f"Chunking and embedding scraped content for competitor {competitor_id} from {url}")
    
    doc = Document(
        page_content=content,
        metadata={
            "competitor_id": competitor_id,
            "url": url,
            "source_type": "website",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )
    
    chunks = text_splitter.split_documents([doc])
    
    if chunks:
        vector_store.add_documents(chunks)
        logger.info(f"Stored {len(chunks)} vector chunks in ChromaDB for URL {url}")
    else:
        logger.warning(f"No text extracted or chunked for URL {url}")


async def store_news_article(competitor_name: str, article: Dict[str, Any]) -> None:
    """
    Stores a news article in ChromaDB for later RAG retrieval.
    """
    url = article.get("url")
    title = article.get("title") or "Untitled Article"
    logger.info(f"Embedding news article: {title}")
    
    content = f"Title: {title}\n\nSummary: {article.get('description', '')}"
    
    doc = Document(
        page_content=content,
        metadata={
            "competitor_name": competitor_name,
            "url": url if url else "",
            "source": article.get("source", "Unknown"),
            "source_type": "news",
            "published_at": article.get("published_at", ""),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )
    
    chunks = text_splitter.split_documents([doc])
    if chunks:
        vector_store.add_documents(chunks)
        logger.info(f"Stored news article '{title[:30]}...' in ChromaDB.")


def get_vector_store() -> Chroma:
    """
    Returns the shared ChromaDB Chroma instance.
    Used by the Chat API for RAG retrieval.
    """
    return vector_store
