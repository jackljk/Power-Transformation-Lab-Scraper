from browser_use import Agent
import os
import glob
import re
import logging

from utils.scraper_utils import save_to_pdf

logger = logging.getLogger(__name__)

async def save_page_content(agent):
    """Hook to save the page content at the end of the step if data was successfully scraped.

    Args:
        agent (_type_): _description_
    """
    # Make sure we have state history
    if hasattr(agent, "state"):
        history = agent.state.history
    else:
        history = None
        logging.warning("No state history found. Skipping page content saving.")
        return
    
    # we only want to save content if during this step we scraped data
    # get models last
    
    
    
    
    
    # Setup the results path + webpage number
    results_env = os.getenv("RESULTS_PATH")
    if not results_env:
        logging.error("RESULTS_PATH environment variable is not set. Skipping page content saving.")
        return
    results_path = os.path.join(results_env, "local")
    urls = agent.state.history.urls()
    current_url, webpage_number = urls[-1], len(urls)
    if not os.path.exists(f"{results_path}/webpage-{webpage_number}"):
        os.makedirs(f"{results_path}/webpage-{webpage_number}/")
    
    
    # Capture the page content
    browser_context = agent.browser_context
    website_html = await browser_context.get_page_html()
    website_screenshot = await browser_context.take_screenshot()
    page = await browser_context.get_current_page()
    
    # save page as pdf
    await save_to_pdf(current_url, page, results_path, webpage_number)
    
    # print the full file path
    file_path = f"{results_path}/webpage-{webpage_number}/webpage-{webpage_number}.pdf"
    
    
    return 