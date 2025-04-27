"""
LLM configuration settings for language models.
"""
import logging
from ..config_manager import config_manager

logger = logging.getLogger(__name__)

# LLM provider and model
LLM_PROVIDER = config_manager.get("llm_config.llm.provider")
if not LLM_PROVIDER:
    raise ValueError("LLM_PROVIDER must be specified in the configuration.")

LLM_MODEL = config_manager.get("llm_config.llm.model")
if not LLM_MODEL:
    raise ValueError("LLM_MODEL must be specified in the configuration.")

# Hyperparameters
LLM_TEMPERATURE = config_manager.get("llm_config.hyperparameters.temperature", 0.7)
LLM_MAX_TOKENS = config_manager.get("llm_config.hyperparameters.max_tokens", 1000)
LLM_TOP_P = config_manager.get("llm_config.hyperparameters.top_p", 1.0)
LLM_FREQUENCY_PENALTY = config_manager.get(
    "llm_config.hyperparameters.frequency_penalty", 0.0
)
LLM_PRESENCE_PENALTY = config_manager.get(
    "llm_config.hyperparameters.presence_penalty", 0.0
)

# LLM API Keys
OPENAI_API_KEY = config_manager.get_secret("secrets.llm.openai.api_key")
ANTHROPIC_API_KEY = config_manager.get_secret("secrets.llm.anthropic.api_key")
GOOGLE_API_KEY = config_manager.get_secret("secrets.llm.google.api_key")
DEEPSEEK_API_KEY = config_manager.get_secret("secrets.llm.deepseek.api_key")
AZURE_API_KEY = config_manager.get_secret("secrets.llm.azure.api_key")
AZURE_ENDPOINT = config_manager.get_secret("secrets.llm.azure.endpoint")

# Validate API keys
if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is required when using OpenAI as provider")
elif LLM_PROVIDER == "deepseek" and not DEEPSEEK_API_KEY:
    raise ValueError("DeepSeek API key is required when using DeepSeek as provider")
elif LLM_PROVIDER == "anthropic" and not ANTHROPIC_API_KEY:
    raise ValueError("Anthropic API key is required when using Anthropic as provider")
elif LLM_PROVIDER == "azure_openai" and not AZURE_API_KEY and not AZURE_ENDPOINT:
    raise ValueError(
        "Azure OpenAI API key and endpoint are required when using Azure OpenAI as provider"
    )
elif LLM_PROVIDER == "google" and not GOOGLE_API_KEY:
    raise ValueError("Google API key is required when using Google as provider")

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