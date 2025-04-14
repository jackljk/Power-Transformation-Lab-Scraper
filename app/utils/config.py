import os
from .config_manager import config_manager

###################################################################################
# Browser-use Agent configuration
###################################################################################
USE_VISION = config_manager.get(
    "agent_config.agent.use_vision", 
    False
)

SAVE_CONVERSATION_PATH = config_manager.get(
    "agent_config.agent.save_conversation_path", 
    None
)

RUN_MAX_STEPS = int(config_manager.get(
    "agent_config.agent_run.max_steps", 
    100
))

###################################################################################
# Browser-use browser configuration
###################################################################################

# Browser-use configuration using ConfigManager - no env var fallbacks
BROWSERUSE_HEADLESS = config_manager.get(
    "browser_config.browser.headless", 
    True
)

# Convert time values to milliseconds as needed
BROWSERUSE_MIN_WAIT_PAGE_LOAD_TIME = int(config_manager.get(
    "browser_config.browser.wait_times.min_page_load", 
    1
))

BROWSERUSE_MAX_WAIT_PAGE_LOAD_TIME = int(config_manager.get(
    "browser_config.browser.wait_times.max_page_load", 
    5
))

BROWSER_TIMEOUT = int(config_manager.get(
    "browser_config.browser.wait_times.timeout", 
    30
))

# Window size configuration
window_width = config_manager.get("browser_config.browser.window.width", 1920)
window_height = config_manager.get("browser_config.browser.window.height", 1080)
BROWSERUSE_WINDOW_SIZE = {'width': window_width, 'height': window_height}

# Debug settings
BROWSERUSE_HIGHLIGHT_ELEMENTS = config_manager.get(
    "browser_config.browser.debug.highlight_elements", 
    True
)

# Recording paths
BROWSERUSE_SAVE_RECORDING_PATH = config_manager.get(
    "browser_config.browser.recordings.save_path", 
    None
)

BROWSERUSE_TRACE_PATH = config_manager.get(
    "browser_config.browser.recordings.trace_path", 
    None
)
###################################################################################
# LLM configuration
###################################################################################
LLM_PROVIDER = config_manager.get("llm_config.llm.provider")
if not LLM_PROVIDER:
    raise ValueError("LLM_PROVIDER must be specified in the configuration.")

LLM_MODEL = config_manager.get("llm_config.llm.model")
if not LLM_MODEL:
    raise ValueError("LLM_MODEL must be specified in the configuration.")

LLM_TEMPERATURE = config_manager.get("llm_config.hyperparameters.temperature", 0.7)
LLM_MAX_TOKENS = config_manager.get("llm_config.hyperparameters.max_tokens", 1000)
LLM_TOP_P = config_manager.get("llm_config.hyperparameters.top_p", 1.0)
LLM_FREQUENCY_PENALTY = config_manager.get("llm_config.hyperparameters.frequency_penalty", 0.0)
LLM_PRESENCE_PENALTY = config_manager.get("llm_config.hyperparameters.presence_penalty", 0.0)

# LLM API Key
OPENAI_API_KEY = config_manager.get_secret("secrets.llm.openai.api_key")
ANTHROPIC_API_KEY = config_manager.get_secret("secrets.llm.anthropic.api_key")
GOOGLE_API_KEY = config_manager.get_secret("secrets.llm.google.api_key")
DEEPSEEK_API_KEY = config_manager.get_secret("secrets.llm.deepseek.api_key")
AZURE_API_KEY = config_manager.get_secret("secrets.llm.azure.api_key")
AZURE_ENDPOINT = config_manager.get_secret("secrets.llm.azure.endpoint")


# Raise error if required API key for selected provider is missing
if LLM_PROVIDER in ["openai", "deepseek"] and not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is required when using OpenAI as provider")
elif LLM_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
    raise ValueError("Anthropic API key is required when using Anthropic as provider")
elif LLM_PROVIDER == "azure_openai" and not AZURE_API_KEY and not AZURE_ENDPOINT:
    raise ValueError("Azure OpenAI API key and endpoint are required when using Azure OpenAI as provider")
elif LLM_PROVIDER == "google" and not GOOGLE_API_KEY:
    raise ValueError("Google API key is required when using Google as provider")


# Application configuration moved to YAML
DEBUG_MODE = config_manager.get("browser_config.debug_mode", False)

# Function to handle getting the LLM instance based on the provider
def get_llm_config():
    """Get the LLM configuration based on the provider."""
    config = {
        "provider": LLM_PROVIDER,
        "model": LLM_MODEL,
        "temperature": LLM_TEMPERATURE,
        "max_tokens": LLM_MAX_TOKENS,
        "top_p": LLM_TOP_P,
        "frequency_penalty": LLM_FREQUENCY_PENALTY,
        "presence_penalty": LLM_PRESENCE_PENALTY,
    }
    
    if LLM_PROVIDER == "openai":
        config["api_key"] = OPENAI_API_KEY
    elif LLM_PROVIDER == "deepseek":
        config["api_key"] = DEEPSEEK_API_KEY
    elif LLM_PROVIDER == "anthropic":
        config["api_key"] = ANTHROPIC_API_KEY
    elif LLM_PROVIDER == "azure_openai":
        config["api_key"] = AZURE_API_KEY
        config["endpoint"] = AZURE_ENDPOINT
    elif LLM_PROVIDER == "google":
        config["api_key"] = GOOGLE_API_KEY
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")
    
    return config

# Function to reload all configurations
def reload_config():
    """Reload all configuration files."""
    config_manager.reload()