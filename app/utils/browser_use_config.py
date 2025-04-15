# Import updated configuration
from browser_use.browser.context import BrowserContextConfig

def define_browser_use_context():
    """
    Define the browser-use configuration using the BrowserConfig class.S
    
    This function initializes the browser configuration with the specified parameters.
    """
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
    return BrowserContextConfig(
        minimum_wait_page_load_time =BROWSERUSE_MIN_WAIT_PAGE_LOAD_TIME,
        maximum_wait_page_load_time =BROWSERUSE_MAX_WAIT_PAGE_LOAD_TIME,
        browser_window_size =BROWSERUSE_WINDOW_SIZE,
        highlight_elements=BROWSERUSE_HIGHLIGHT_ELEMENTS,
        save_recording_path=BROWSERUSE_SAVE_RECORDING_PATH,
        trace_path=BROWSERUSE_TRACE_PATH,
        cookies_file="path/to/cookies.json",
        locale='en-US',
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        allowed_domains=['google.com', 'wikipedia.org'],
    )