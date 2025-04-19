import os
import logging
import re

logger = logging.getLogger(__name__)

async def save_to_pdf(current_url, page, results_path, webpage_number):
    short_url = re.sub(r'^https?://(?:www\\.)?|/$', '', current_url)
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', short_url).strip('-').lower() 
    if os.path.exists(f"{results_path}/webpage-{webpage_number}/{slug}.pdf"):
        logger.info(f"PDF already exists for {current_url}. Skipping PDF generation.")
        return
    
    # save page as pdf
    await page.emulate_media(media='screen')
    await page.pdf(path=f"{results_path}/webpage-{webpage_number}/{slug}.pdf" , format='A4', print_background=False)