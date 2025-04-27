import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional
import sys
from pathlib import Path
import glob


from utils.config import DEBUG_MODE, load_custom_config, parse_local_config
from utils.config_manager import config_manager
from utils.logging import setup_results_path

from models.tasks_models import Task


# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def scrape_url(
    url: str,
    prompt: str,
    additional_context: Optional[Dict[str, Any]] = None,
    task_template: str = "default",
    initial_actions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
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
    from services.scraper import WebScraper
    try:
        logger.info(f"Scraping {url} for information about: {prompt}")
        scraper = WebScraper(
            url=url,
            prompt=prompt,
            additional_context=additional_context,
            task_template=task_template,
            initial_actions=initial_actions,
        )
        result = await scraper.scrape()
        return result
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        raise


async def main():
    # Call the function at the start of main
    if not load_custom_config():
        logger.error("Scraper shutting down please check your config file")
        return
    
    # get all available templates
    templates = Task.get_available_templates()

    local_config = parse_local_config(templates)
    
    # Set output path to a environment variable if provided to be accessible everywhere in the app
    profile_name = local_config.get("profile_name")
    output_path = local_config.get("output_path")
    setup_results_path(output_path, profile_name)
        
    # Scrape the URL
    result = await scrape_url(
        url=local_config.get("url"),
        prompt=local_config.get("prompt"),
        additional_context=local_config.get("additional_context"),
        task_template=local_config.get("task_template", "default"),
        initial_actions=local_config.get("initial_actions", []),
    )
    
    # TODO: Handle different output formats
    # Format the result as JSON
    formatted_result = json.dumps(result, indent=2)

    results_env = os.getenv("RESULTS_PATH")
    if not results_env:
        logging.error("RESULTS_PATH environment variable is not set. Skipping page content saving.")
        return
    results_path = os.path.join(results_env, "output.json")
    with open(results_path, "w") as f:
        f.write(formatted_result)

if __name__ == "__main__":
    asyncio.run(main())
