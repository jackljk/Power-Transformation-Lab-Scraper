from pydantic import BaseModel, Field
from typing import List, Optional, Type, Dict, Any, Union
from app.utils.config.local import build_content_model
from pydantic.main import create_model


# class Citation(BaseModel):
#     """
#     Model representing a citation with text, location and confidence.
#     """
#     source_text: str = Field(..., description="The exact text from the webpage where the data extracted was found")
#     location: str = Field(..., description="Description of where this was found")
#     location_url: str = Field(..., description="URL of the location where the text was found using a link highlight")

def build_output_model(content_structure: Union[Dict, Any]) -> Type[BaseModel]:
    """
    Build the ScraperOutputList model dynamically based on the ScraperOutput model.
    This allows for handling multiple outputs from the scraper.
    """
    output_model = _generate_scraper_output_structure(content_structure)
    # Define the fields for the ScraperOutputList model
    fields = {
        "outputs": (List[output_model], Field(..., description="List of ScraperOutput objects")),
    }
    
    # Create and return the ScraperOutputList model
    return create_model("ScraperOutputList", **fields)

def _generate_scraper_output_structure(content_structure: Union[Dict, Any]) -> Type[BaseModel]:
    """
    Build the ScraperOutput model dynamically based on the content structure.
    This allows for flexibility in the output format.
    """
    # Define the fields for the ScraperOutput model
    content_model = build_content_model(content_structure)
    content_model_name = next(iter(content_structure.keys()), "")
    fields = {
        f"{content_model_name}-content": (List[content_model], Field(..., description="Extracted information in the most appropriate format")),
        "format_type": (str, Field(default="text", description="Format type of the content (json/table/text/etc.)")),
        "summary": (Optional[str], Field(None, description="Brief summary of the information found")),
    }
    
    # Create and return the ScraperOutput model
    return create_model("ScraperOutput", **fields)

