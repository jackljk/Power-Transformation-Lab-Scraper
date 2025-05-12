"""
Main configuration module that imports and re-exports all configuration components.
This provides a unified interface for importing configuration settings throughout the app.
"""
import logging
from .config_manager import config_manager

# Import configuration components from individual modules
from .config.browser_use_agent import (
    USE_VISION,
    SAVE_CONVERSATION_PATH,
    RUN_MAX_STEPS,
    USE_PLANNER_MODEL,
    PLANNER_INTERVAL,
    DEBUG_MODE,
)

from .config.browser import (
    BROWSERUSE_HEADLESS,
    BROWSERUSE_MIN_WAIT_PAGE_LOAD_TIME,
    BROWSERUSE_MAX_WAIT_PAGE_LOAD_TIME,
    BROWSER_TIMEOUT,
    BROWSERUSE_WINDOW_SIZE,
    BROWSERUSE_HIGHLIGHT_ELEMENTS,
    BROWSERUSE_SAVE_RECORDING_PATH,
    BROWSERUSE_TRACE_PATH,
)

from .config.llm import (
    LLM_PROVIDER,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    LLM_TOP_P,
    LLM_FREQUENCY_PENALTY,
    LLM_PRESENCE_PENALTY,
    OPENAI_API_KEY,
    ANTHROPIC_API_KEY,
    GOOGLE_API_KEY,
    DEEPSEEK_API_KEY,
    AZURE_API_KEY,
    AZURE_ENDPOINT,
    get_llm_config,
)

from .config.local import (
    load_profile_config,
    build_content_model,
    parse_local_config,
)

logger = logging.getLogger(__name__)

# Function to reload all configurations
def reload_config():
    """Reload all configuration files."""
    config_manager.reload()
