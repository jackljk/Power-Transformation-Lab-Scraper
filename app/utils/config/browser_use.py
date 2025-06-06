# Import updated configuration
from browser_use import BrowserSession, BrowserProfile
import logging
from ..config_manager import config_manager
import os

"""
Browser configuration settings for browser-use.
"""
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
    "browser_config.browser.recordings.save_path", False
)

BROWSERUSE_TRACE_PATH = config_manager.get(
    "browser_config.browser.recordings.trace_path", False
)


def define_browser_use_session():
    """
    Define the browser-use configuration using the BrowserConfig class.

    This function initializes the browser configuration with the specified parameters.
    """

    # append main results path to recording paths
    results_env = os.getenv("RESULTS_PATH")
    if not results_env:
        logger.error(
            "RESULTS_PATH environment variable is not set. Skipping PDF response logging."
        )
        return

    # set the recording paths to the main results path
    browser_use_recording_path = (
        os.path.join(
            results_env,
            "recordings",
        )
        if BROWSERUSE_SAVE_RECORDING_PATH
        else None
    )

    browser_use_trace_path = (
        os.path.join(
            results_env,
            "traces",
        )
        if BROWSERUSE_TRACE_PATH
        else None
    )

    # set download save path (not a config option)
    downloads_dir = (
        os.path.join(
            results_env,
            "downloads",
        )
        if BROWSERUSE_SAVE_RECORDING_PATH
        else "downloads"
    )

    # Create browser context config with properly formatted parameters
    # Updated to match the current browser-use API
    browser_profile = BrowserProfile(
        minimum_wait_page_load_time=BROWSERUSE_MIN_WAIT_PAGE_LOAD_TIME,
        maximum_wait_page_load_time=BROWSERUSE_MAX_WAIT_PAGE_LOAD_TIME,
        highlight_elements=BROWSERUSE_HIGHLIGHT_ELEMENTS,
        locale="en-US",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        allowed_domains=None,
        headless=BROWSERUSE_HEADLESS,
        disable_security=True,
        user_data_dir='~/.config/browseruse/profiles/default',
        save_recording_path= browser_use_recording_path,
        trace_path=browser_use_trace_path,
    )

    browser_session = BrowserSession(
        browser_profile=browser_profile,
        # Any session-specific overrides can go here
    )

    return browser_session
