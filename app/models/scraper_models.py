from pydantic import BaseModel, AnyUrl
from typing import Dict, Any, Optional, List


class Citation(BaseModel):
    """Model for storing citation information from scraped content"""
    text: str
    source_url: str
    selector_path: Optional[str] = None
    confidence_score: float


class ScrapedResult(BaseModel):
    """Model for the formatted result from the scraper"""
    content: Any
    citations: List[Citation]
    format_type: str  # Can be 'json', 'text', 'structured', etc.
    prompt: str
    url: str


class ScrapeRequest(BaseModel):
    """Model for the scrape request"""
    url: AnyUrl
    prompt: str
    additional_context: Optional[Dict[str, Any]] = None