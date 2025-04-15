import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional
import sys
from pathlib import Path

from services.scraper import WebScraper
from utils.config import DEBUG_MODE
from utils.config_manager import config_manager
from models.tasks_models import Task

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def scrape_url(url: str, prompt: str, additional_context: Optional[Dict[str, Any]] = None, task_template: str = "default") -> Dict[str, Any]:
    """
    Scrape a website for information based on a prompt.
    
    Args:
        url: The URL to scrape
        prompt: What information to extract from the website
        additional_context: Optional additional context to help with scraping
        task_template: The template to use for scraping (default, summary, detailed, qa)
            
    Returns:
        A structured result containing the extracted information with citations
    """
    try:
        logger.info(f"Scraping {url} for information about: {prompt}")
        scraper = WebScraper(
            url=url,
            prompt=prompt,
            additional_context=additional_context,
            task_template=task_template
        )
        result = await scraper.scrape()
        return result
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        raise


async def main():
    # Check for custom config file specified as command-line argument
    # This is a minimal fallback for when you need to specify a different config
    if len(sys.argv) > 1 and sys.argv[1].endswith('.yaml'):
        config_override = sys.argv[1]
        config_path = Path(config_override)
        if config_path.exists():
            logger.info(f"Loading config override: {config_override}")
            config_manager.load_specific_config("local", str(config_path))
        else:
            logger.error(f"Config file not found: {config_override}")
            return
    
    # Get scraper parameters from configuration - now using local.yaml
    url = config_manager.get("local.scraper.url")
    prompt = config_manager.get("local.scraper.prompt")
    
    # Validate required configuration
    if not url:
        logger.error("URL is required in configuration (local.scraper.url)")
        return
    
    if not prompt:
        logger.error("Prompt is required in configuration (local.scraper.prompt)")
        return
    
    # Parse additional context if provided
    additional_context = None
    context_config = config_manager.get("local.scraper.context", {})
    
    if context_config and context_config.get("value"):
        context_format = context_config.get("format", "json")
        context_value = context_config.get("value")
        
        if context_format == "json":
            try:
                additional_context = json.loads(context_value)
            except json.JSONDecodeError:
                logger.warning("Failed to parse context as JSON. Using as plain text.")
                additional_context = {"text": context_value}
        else:
            additional_context = {"text": context_value}
    
    # Get task template
    available_templates = Task.get_available_templates()
    task_template = config_manager.get("local.scraper.task_template", "default")
    
    # Validate template choice
    if task_template not in available_templates:
        logger.warning(f"Invalid template: {task_template}. Using default template instead.")
        task_template = "default"
    
    # Scrape the URL
    result = await scrape_url(
        url=url,
        prompt=prompt,
        additional_context=additional_context,
        task_template=task_template
    )
    # TODO: Handle different output formats
    # Format the result as JSON
    formatted_result = json.dumps(result, indent=2)
    
    # Output the result
    output_path = config_manager.get("local.scraper.output_path")
    if output_path:
        # Handle relative paths by resolving them relative to the script location
        if not os.path.isabs(output_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.normpath(os.path.join(script_dir, output_path))
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write results to file
        with open(output_path, 'w') as f:
            f.write(formatted_result)
        logger.info(f"Results saved to {output_path}")
    else:
        print(formatted_result)


if __name__ == "__main__":
    asyncio.run(main())