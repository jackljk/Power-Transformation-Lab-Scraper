import os
from typing import Dict, Any, Optional, List
import json
from pydantic import BaseModel

# Import browser-use for web scraping with AI
from browser_use import BrowserUse
from app.utils.config import BROWSER_HEADLESS, BROWSER_TIMEOUT


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


class WebScraper:
    """
    A web scraper class that uses browser-use to extract targeted information
    from websites based on user prompts.
    """
    
    def __init__(self):
        """
        Initialize the WebScraper.
        """
        self.browser = BrowserUse(headless=BROWSER_HEADLESS, timeout=BROWSER_TIMEOUT)
    
    async def scrape(self, url: str, prompt: str, additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Scrape a website for information based on a prompt.
        
        Args:
            url: The URL to scrape
            prompt: What information to extract from the website
            additional_context: Any additional context that may help with scraping
            
        Returns:
            A structured result containing the extracted information with citations
        """
        try:
            # Navigate to the URL
            await self.browser.goto(url)
            
            # Formulate the task for the AI
            task = f"""
            From the provided webpage, extract information about: "{prompt}"
            
            Requirements:
            1. The extracted information must be 100% factual and found on the page.
            2. For each piece of information, provide a citation with the exact text and location from the webpage.
            3. Analyze the extracted information and determine the most appropriate format for returning it.
            4. Assign a confidence score (0.0-1.0) for each citation based on how directly it addresses the prompt.
            5. Only include information that is relevant to the prompt.
            
            Additional context: {additional_context if additional_context else "None provided"}
            
            Format the output as a JSON with the following structure:
            {{
                "content": [extracted information in the most appropriate format],
                "citations": [
                    {{
                        "text": "exact text from webpage",
                        "location": "description of where this was found",
                        "confidence": 0.95
                    }}
                ],
                "format_type": "json/table/text/etc based on content type",
                "summary": "brief summary of the information found"
            }}
            """
            
            # Use BrowserUse's ai_chat to extract information
            result = await self.browser.ai_chat(task)
            
            # Process the AI response
            processed_result = self._process_ai_response(result, url, prompt)
            return processed_result.model_dump()
        finally:
            # Close the browser after scraping
            await self.browser.close()
    
    def _process_ai_response(self, ai_response: str, url: str, prompt: str) -> ScrapedResult:
        """
        Process the AI response into a structured format with citations.
        
        Args:
            ai_response: The raw response from the AI
            url: The original URL that was scraped
            prompt: The original prompt
            
        Returns:
            A ScrapedResult object with structured data and citations
        """
        # Try to parse as JSON first
        try:
            # Check if the response contains JSON
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = ai_response[json_start:json_end]
                data = json.loads(json_str)
                
                # Try to extract citations if they exist
                citations_data = data.get("citations", [])
                citations = [
                    Citation(
                        text=c.get("text", ""),
                        source_url=url,
                        selector_path=c.get("location", ""),
                        confidence_score=float(c.get("confidence", 0.5))
                    )
                    for c in citations_data if isinstance(c, dict)
                ]
                
                # Get content and format type
                content = data.get("content", data)
                format_type = data.get("format_type", "json")
                
                return ScrapedResult(
                    content=content,
                    citations=citations if citations else [
                        Citation(
                            text="Extracted from webpage",
                            source_url=url,
                            selector_path="",
                            confidence_score=0.7
                        )
                    ],
                    format_type=format_type,
                    prompt=prompt,
                    url=url
                )
                
        except:
            # If JSON parsing failed, proceed with text processing
            pass
        
        # Determine the best format for the data based on the content
        format_type = self._determine_best_format(ai_response)
        
        # Default citation when no specific citations are extracted
        sample_citations = [
            Citation(
                text="Information extracted from webpage",
                source_url=url,
                selector_path="",
                confidence_score=0.7
            )
        ]
            
        return ScrapedResult(
            content=ai_response,
            citations=sample_citations,
            format_type=format_type,
            prompt=prompt,
            url=url
        )
    
    def _determine_best_format(self, content: str) -> str:
        """
        Determine the best format for the extracted data based on its structure.
        
        Args:
            content: The extracted content to analyze
            
        Returns:
            A string representing the best format (json, text, structured, etc.)
        """
        # Check if it looks like JSON
        if isinstance(content, str):
            if content.strip().startswith('{') and content.strip().endswith('}'):
                return "json"
            
            # Check if it contains tabular data
            if '\n' in content and '|' in content:
                return "table"
            
            # Check if it seems to be a list
            if content.strip().startswith('[') and content.strip().endswith(']'):
                return "list"
        
        # Default to text format
        return "text"