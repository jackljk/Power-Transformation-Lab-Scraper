from pydantic import BaseModel, Field
from typing import List, Optional
from app.utils.config.local import build_content_model

ContentModel = build_content_model()

class Citation(BaseModel):
    """
    Model representing a citation with text, location and confidence.
    """
    source_text: str = Field(..., description="The exact text from the webpage where the data extracted was found")
    location: str = Field(..., description="Description of where this was found")
    location_url: str = Field(..., description="URL of the location where the text was found using a link highlight")


class ScraperOutput(BaseModel):
    """
    Standard output format model for browser-use scraping results.
    This model will be used with browser-use's Controller for structured output.
    """
    content: List[ContentModel] = Field(  # type: ignore
        ..., 
        description="Extracted information in the most appropriate format"
    )
    # citations: List[Citation] = Field(
    #     default_factory=list,
    #     description="List of citations for the extracted information"
    # )
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