import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional
import sys
from pathlib import Path

from services.scraper import WebScraper
from utils.config import DEBUG_MODE, load_custom_config, parse_local_config
from utils.config_manager import config_manager
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
        return

    # get all available templates
    templates = Task.get_available_templates()

    local_config = parse_local_config(templates)

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

    # Output the result
    output_path = local_config.get("output_path")
    if output_path:
        # Handle relative paths by resolving them relative to the script location
        if not os.path.isabs(output_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.normpath(os.path.join(script_dir, output_path))

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Write results to file
        with open(output_path, "w") as f:
            f.write(formatted_result)
        logger.info(f"Results saved to {output_path}")
    else:
        print(formatted_result)


if __name__ == "__main__":
    asyncio.run(main())
