from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union


class Citation(BaseModel):
    """
    Model representing a citation with text, location and confidence.
    """
    text: str = Field(..., description="The exact text from the webpage")
    location: str = Field(..., description="Description of where this was found")
    confidence: float = Field(default=0.7, description="Confidence score (0.0-1.0) for the citation")
    
class ScraperOutput(BaseModel):
    """
    Standard output format model for browser-use scraping results.
    This model will be used with browser-use's Controller for structured output.
    """
    content: Union[str, Dict[str, Any], List[Dict[str, Any]]] = Field(
        ..., 
        description="Extracted information in the most appropriate format"
    )
    citations: List[Citation] = Field(
        default_factory=list,
        description="List of citations for the extracted information"
    )
    format_type: str = Field(
        default="text", 
        description="Format type of the content (json/table/text/etc.)"
    )
    summary: Optional[str] = Field(
        None, 
        description="Brief summary of the information found"
    )
    
class ScraperOutputList(BaseModel):
    """
    Model representing a list of ScraperOutput objects.
    This is used to handle multiple outputs from the scraper.
    """
    outputs: List[ScraperOutput]