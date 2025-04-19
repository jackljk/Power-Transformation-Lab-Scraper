import os
from .config_manager import config_manager
import sys
from pathlib import Path
import logging
import json
from pydantic import BaseModel, Field, create_model


logger = logging.getLogger(__name__)


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


####################################################################################
# Local configuration
####################################################################################
def load_custom_config() -> bool:
    """
    Load a custom configuration file specified as a command-line argument or from local config.
    
    Returns:
        bool: True if custom config was loaded successfully, False otherwise
    """
    # Check for command-line override first
    if len(sys.argv) > 1 and sys.argv[1].endswith('.yaml'):
        config_override = sys.argv[1]
        config_path = Path(config_override)
        if config_path.exists():
            logger.info(f"Loading config override from command line: {config_override}")
            config_manager.load_specific_config("local", str(config_path))
            return True
        else:
            logger.error(f"Config file not found: {config_override}")
            return False
    
    # If no command-line override, check for profile reference in local.yaml
    profile_name = config_manager.get("local.profile")
    if profile_name:
        # Build the profile path relative to config directory
        profile_path = Path(config_manager.config_dir) / "profiles" / f"{profile_name}.yaml"
        if profile_path.exists():
            logger.info(f"Loading profile: {profile_name}")
            config_manager.load_specific_config("profile", str(profile_path))
            return True
        else:
            logger.error(f"Profile not found: {profile_name}")
            logger.error(f"Expected path: {profile_path}")
            return False
    
    # No override specified, continue with default local config
    return True

# returns a pydantic model of the content format
def build_content_model() -> BaseModel:
    """
    Parse the content format from the configuration and return the corresponding model.
    """
    # First check for content structure in profile if it exists
    content_structure = config_manager.get("profile.content_structure")
    
    # Fall back to local config if not found in profile
    if not content_structure:
        content_structure = config_manager.get("local.content_structure")
    
    # If no content structure defined anywhere, return a generic model
    if not content_structure:
        # Create a simple default model for text content
        return create_model("TextContent", text=(str, ...))
    
    type_map = {
        "str": (str, ...),
        "int": (int, ...),
        "float": (float, ...),
        "bool": (bool, ...)
    }
    
    model_name, fields = next(iter(content_structure.items()))
    model_fields = {k: type_map[v] for k, v in fields.items()}
    
    content_model = create_model(model_name, **model_fields)
    return content_model
    

def parse_local_config(available_templates: list) -> dict:
    """
    Parse the configuration from profile and/or local configs and set up the environment.
    
    Args:
        available_templates: List of available task templates
        
    Returns:
        dict: Dictionary of configuration values
    """
    # Helper function to get config with profile fallback
    def get_config(key, default=None):
        # Only look in profile configuration, as local should only contain profile reference
        # and optional overrides that should be explicitly checked
        value = config_manager.get(f"profile.scraper.{key}")
        
        # Only check local for explicit overrides, not as fallback for missing values
        if value is None and key in ["url", "prompt", "output_path", "task_template"]:
            local_value = config_manager.get(f"local.scraper.{key}")
            if local_value is not None:
                logger.info(f"Using override from local config for: {key}")
                return local_value
        
        return value if value is not None else default
    
    # Get required configuration
    url = get_config("url")
    prompt = get_config("prompt")
    
    # Validate required configuration
    if not url:
        logger.error("URL is required in profile configuration (profile.scraper.url)")
        return {}
    
    if not prompt:
        logger.error("Prompt is required in profile configuration (profile.scraper.prompt)")
        return {}
    
    # Handle additional context
    additional_context = None
    context_config = get_config("context", {})
    if context_config and context_config.get("value"):
        context_format = context_config.get("format")
        context_value = context_config.get("value")
        
        if context_format == "json":
            try:
                additional_context = json.loads(context_value)
                additional_context = "\n".join([f"{k}: {v}" for k, v in additional_context.items()])
            except json.JSONDecodeError:
                logger.warning("Failed to parse context as JSON. Using as plain text.")
                additional_context = context_value
        else:
            additional_context = context_value
    
    # Handle initial actions
    initial_actions = get_config("initial_actions", [])
    if initial_actions:
        parsed_initial_actions = []
        for initial_action in initial_actions:
            action, value = list(initial_action.items())[0]
            if 'scroll' in action:
                parsed_initial_actions.append({action: {"amount": value}})
            elif 'go_to_url' == action:
                parsed_initial_actions.append({action: {"url": value}})
            else:
                logger.warning(f"Unknown action: {action}. Skipping.")
                continue
        initial_actions = parsed_initial_actions
    
    # Set the task template
    task_template = get_config("task_template", "default")
    
    if task_template not in available_templates:
        logger.warning(f"Invalid template: {task_template}. Using default template instead.")
        task_template = "default"
    
    # Get output path
    output_path = get_config("output_path")
    
    # Return all configuration values
    return {
        "url": url,
        "prompt": prompt,
        "additional_context": additional_context,
        "task_template": task_template,
        "initial_actions": initial_actions,
        "output_path": output_path,
        "debug_mode": DEBUG_MODE,
    }
        
    



# Function to reload all configurations
def reload_config():
    """Reload all configuration files."""
    config_manager.reload()