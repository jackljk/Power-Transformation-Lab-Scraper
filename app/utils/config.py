import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Browser-use configuration
BROWSER_HEADLESS = os.getenv('BROWSER_HEADLESS', 'true').lower() == 'true'
BROWSER_TIMEOUT = int(os.getenv('BROWSER_TIMEOUT', '30000'))  # milliseconds

# Application configuration
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'