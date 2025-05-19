import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any, Optional
import warnings
import tracemalloc

from app.utils.config.local import load_profile_config, parse_local_config
from app.utils.config_manager import config_manager
from app.utils.logging import setup_results_path
from app.utils.config.browser_use_agent import DEBUG_MODE

from app.models.tasks_models import Task
from app.utils.scraper_utils import cleanup_resources

# Start memory tracking
tracemalloc.start()
warnings.simplefilter("always", RuntimeWarning)



# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# # ignore resource warnings
# warnings.filterwarnings("ignore", category=ResourceWarning)
# # Use WindowsSelectorEventLoopPolicy for Windows
# if os.name == "nt":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def scrape_url(
    scraper_type: str, # ["browser_use", "bright_data_mcp"]
    prompt: str,
    url: Optional[str] = None,
    filepath: Optional[str] = None,
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
    from app.models.output_format_models import build_output_model
    
    content_structure = config_manager.get("profile.content_structure")
    
    try:
        if scraper_type == "browser_use":
            from app.services.browser_use_scraper import WebScraper
            logger.info("Using browser_use for scraping")
            logger.info(f"Scraping {url} for information about: {prompt}")
            
            scraper = WebScraper(
                url=url,
                prompt=prompt,
                additional_context=additional_context,
                task_template=task_template,
                initial_actions=initial_actions,
                output_format=build_output_model(content_structure),
            )
            result = await scraper.scrape()
            return result
        elif scraper_type == "bright_data_mcp":
            from app.services.brightdata_mcp_scraper import BrightDataMCPScraper
            logger.info("Using bright_data_mcp for scraping")
            logger.info(f"Scraping {url} for information about: {prompt}")
            
            scraper = BrightDataMCPScraper(
                url=url,
                prompt=prompt,
                task_template=task_template,
                additional_context=additional_context,
                output_format=content_structure
            )
            results = await scraper.scrape()
            
            return results
        elif scraper_type == "pdf_scraper":
            from app.services.pdf_scraper import PDFScraper
            logger.info("Using pdf_scraper for scraping")
            logger.info(f"Scraping {url} for information about: {prompt}")
            
            scraper = PDFScraper(
                pdf_paths=filepath,
                prompt=prompt,
                task_template=task_template,
                additional_context=additional_context,
                output_format=content_structure
            )
            result = await scraper.scrape()
            return result
        else:
            logger.error(f"Invalid scraper type: {scraper_type}")
            raise ValueError(f"Invalid scraper type: {scraper_type}")
    except asyncio.CancelledError:
        logger.info("Scraping task was cancelled.")
        raise
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        raise


async def main():
    # Call the function at the start of main
    if not load_profile_config():
        logger.error("Scraper shutting down please check your config file")
        return
    
    # get all available templates
    templates = Task.get_available_templates()

    # get deterministic variables to determine the run type
    local_config = parse_local_config(templates)
    profile_name = local_config.get("profile_name")
    
    
    # Set output path to a environment variable if provided to be accessible everywhere in the app
    output_path = local_config.get("output_path")
    setup_results_path(output_path, profile_name)
    
    try:
        # Scrape the URL
        result = await scrape_url(
            scraper_type=local_config.get("scraper_type", "browser_use"),
            url=local_config.get("url"),
            filepath=local_config.get("filepath", None),
            prompt=local_config.get("prompt"),
            additional_context=local_config.get("additional_context", None),
            task_template=local_config.get("task_template", "default"),
            initial_actions=local_config.get("initial_actions", []),
        )
        # Format the result as JSON
        formatted_result = json.dumps(result, indent=2)

        results_env = os.getenv("RESULTS_PATH")
        if not results_env:
            logging.error("RESULTS_PATH environment variable is not set. Skipping page content saving.")
            return
        results_path = os.path.join(results_env, "output.json")
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        with open(results_path, "w") as f:
            f.write(formatted_result)
            
        logging.info(f"Scraping completed successfully. Results saved to {results_path}")
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        raise
    finally:
        # Clean up any resources if needed
        await cleanup_resources()


if __name__ == "__main__":
    try:
        # Use proper event loop handling for Windows
        if sys.platform == 'win32':
            # Use selector event loop to avoid ProactorEventLoop issues
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(main())
        finally:
            # Properly close the event loop
            pending_tasks = asyncio.all_tasks(loop)
            for task in pending_tasks:
                task.cancel()
                
            # Wait for all tasks to be cancelled
            if pending_tasks:
                loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))
            
            # Close the loop properly
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
            
    except KeyboardInterrupt:
        logger.info("Scraping task was cancelled by user.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

    