import argparse
import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional

from app.services.scraper import WebScraper
from app.utils.config import DEBUG_MODE

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def scrape_url(url: str, prompt: str, additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Scrape a website for information based on a prompt.
    
    Args:
        url: The URL to scrape
        prompt: What information to extract from the website
        additional_context: Optional additional context to help with scraping
            
    Returns:
        A structured result containing the extracted information with citations
    """
    try:
        logger.info(f"Scraping {url} for information about: {prompt}")
        scraper = WebScraper()
        result = await scraper.scrape(
            url=url,
            prompt=prompt,
            additional_context=additional_context
        )
        return result
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        raise


async def main():
    parser = argparse.ArgumentParser(description="Power Transformation Lab Scraper")
    parser.add_argument("--url", "-u", type=str, required=True, help="URL to scrape")
    parser.add_argument("--prompt", "-p", type=str, required=True, help="Information to extract")
    parser.add_argument("--context", "-c", type=str, help="Additional context in JSON format")
    parser.add_argument("--output", "-o", type=str, help="Output file path (default: print to console)")
    
    args = parser.parse_args()
    
    # Parse additional context if provided
    additional_context = None
    if args.context:
        try:
            additional_context = json.loads(args.context)
        except json.JSONDecodeError:
            logger.warning("Failed to parse additional context as JSON. Using as plain text.")
            additional_context = {"text": args.context}
    
    # Scrape the URL
    result = await scrape_url(args.url, args.prompt, additional_context)
    
    # Format the result as JSON
    formatted_result = json.dumps(result, indent=2)
    
    # Output the result
    if args.output:
        with open(args.output, 'w') as f:
            f.write(formatted_result)
        logger.info(f"Results saved to {args.output}")
    else:
        print(formatted_result)


if __name__ == "__main__":
    asyncio.run(main())