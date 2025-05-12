import os
import logging
import re
import asyncio
import sys

logger = logging.getLogger(__name__)

async def save_to_pdf(current_url, page, results_path, webpage_number):
    short_url = re.sub(r'^https?://(?:www\\.)?|/$', '', current_url)
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', short_url).strip('-').lower() 
    
    # limit slug length to 50 characters
    slug = slug[:50] if len(slug) > 50 else slug
    # create directory if it doesn't exist (Just extra measures)
    os.makedirs(f"{results_path}/webpage-{webpage_number}", exist_ok=True)
    
    if os.path.exists(f"{results_path}/webpage-{webpage_number}/{slug}.pdf"):
        logger.info(f"PDF already exists for {current_url}. Skipping PDF generation.")
        return
    
    # save page as pdf
    await page.emulate_media(media='screen')
    await page.pdf(path=f"{results_path}/webpage-{webpage_number}/{slug}.pdf" , format='A4', print_background=False)

async def cleanup_resources():
    """Clean up all async resources properly."""
    # Cancel all pending tasks except the current one
    pending = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]

    if pending:
        logger.debug(f"Cancelling {len(pending)} pending tasks")
        for task in pending:
            task.cancel()

        # Wait for all tasks to be cancelled
        await asyncio.gather(*pending, return_exceptions=True)

    # Close the event loop properly on Windows
    if sys.platform == 'win32':
        loop = asyncio.get_event_loop()
        if hasattr(loop, '_proactor'):
            loop._proactor.close()