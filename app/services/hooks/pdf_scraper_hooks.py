import json
import os
import logging

logger = logging.getLogger(__name__)

def log_response(response):
    """
    Log the response from the PDF scraper.
    """
    # Setup the results path for logging
    results_env = os.getenv("RESULTS_PATH")
    if not results_env:
        logging.error(
            "RESULTS_PATH environment variable is not set. Skipping PDF response logging."
        )
        return
    
    logs_dir = os.path.join(results_env, "pdf_logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Generate a unique filename for this log
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"pdf_response_{timestamp}.json")
    
    # Format the response for logging
    log_data = {
        'timestamp': timestamp,
        'response': response
    }
    
    # Write the log to a file
    try:
        with open(log_filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        logger.info(f"PDF scraper response logged to {log_filename}")
    except Exception as e:
        logger.error(f"Failed to log PDF scraper response: {str(e)}")
