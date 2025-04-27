"""
Browser configuration settings for browser-use.
"""
import logging
from ..config_manager import config_manager

logger = logging.getLogger(__name__)

# Browser-use configuration using ConfigManager - no env var fallbacks
BROWSERUSE_HEADLESS = config_manager.get("browser_config.browser.headless", True)

# Convert time values to milliseconds as needed
BROWSERUSE_MIN_WAIT_PAGE_LOAD_TIME = int(
    config_manager.get("browser_config.browser.wait_times.min_page_load", 1)
)

BROWSERUSE_MAX_WAIT_PAGE_LOAD_TIME = int(
    config_manager.get("browser_config.browser.wait_times.max_page_load", 5)
)

BROWSER_TIMEOUT = int(
    config_manager.get("browser_config.browser.wait_times.timeout", 30)
)

# Window size configuration
window_width = config_manager.get("browser_config.browser.window.width", 1920)
window_height = config_manager.get("browser_config.browser.window.height", 1080)
BROWSERUSE_WINDOW_SIZE = {"width": window_width, "height": window_height}

# Debug settings
BROWSERUSE_HIGHLIGHT_ELEMENTS = config_manager.get(
    "browser_config.browser.debug.highlight_elements", True
)

# Recording paths
BROWSERUSE_SAVE_RECORDING_PATH = config_manager.get(
    "browser_config.browser.recordings.save_path", None
)

BROWSERUSE_TRACE_PATH = config_manager.get(
    "browser_config.browser.recordings.trace_path", None
)