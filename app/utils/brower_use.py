from brower_use import BrowserConfig
# Import updated configuration
from app.utils.config import (
    BROWSERUSE_HEADLESS,
    BROWSER_TIMEOUT,
    BROWSERUSE_WINDOW_SIZE,
    BROWSERUSE_HIGHLIGHT_ELEMENTS,
    BROWSERUSE_SAVE_RECORDING_PATH,
    BROWSERUSE_TRACE_PATH,
    BROWSERUSE_MIN_WAIT_PAGE_LOAD_TIME,
    BROWSERUSE_MAX_WAIT_PAGE_LOAD_TIME
)

def define_browser_use_config():
    """
    Define the browser-use configuration using the BrowserConfig class.
    
    This function initializes the browser configuration with the specified parameters.
    """
    return BrowserConfig(
        headless=BROWSERUSE_HEADLESS,
        min_wait_page_load_time=BROWSERUSE_MIN_WAIT_PAGE_LOAD_TIME,
        max_wait_page_load_time=BROWSERUSE_MAX_WAIT_PAGE_LOAD_TIME,
        timeout=BROWSER_TIMEOUT,
        window_size=BROWSERUSE_WINDOW_SIZE,
        highlight_elements=BROWSERUSE_HIGHLIGHT_ELEMENTS,
        save_recording_path=BROWSERUSE_SAVE_RECORDING_PATH,
        trace_path=BROWSERUSE_TRACE_PATH
    )