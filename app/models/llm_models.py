from typing import Any
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
import logging
import os

from utils.config import get_llm_config

logger = logging.getLogger(__name__)

LLM_CONFIG = get_llm_config()

# Combined dictionary with provider information
LLM_PROVIDERS = {
    "openai": {"class": ChatOpenAI, "endpoint_required": False},
    "google": {"class": ChatGoogleGenerativeAI, "endpoint_required": False},
    "ollama": {"class": ChatOllama, "endpoint_required": False},
    "anthropic": {"class": ChatAnthropic, "endpoint_required": False},
    "azure_openai": {"class": AzureChatOpenAI, "endpoint_required": True},
    "deepseek": {"class": ChatOpenAI, "endpoint_required": False, "custom_url": "https://api.deepseek.com/v1"}
}

def get_llm_instance() -> Any:
    """
    Get an instance of the LLM based on the configuration.
    
    Returns:
        An instance of the LLM class based on the provider specified in the configuration.
    """
    provider = LLM_CONFIG["provider"]
    
    if provider not in LLM_PROVIDERS:
        raise ValueError(f"Unsupported provider: {provider}. Supported providers are: {', '.join(LLM_PROVIDERS.keys())}")
    
    # Common parameters for all providers
    params = {
        "model": LLM_CONFIG["model"],
        "temperature": LLM_CONFIG["temperature"],
    }
    
    # Provider-specific configurations (API keys now set as env vars in config.py)
    if provider == "deepseek":
        params["base_url"] = LLM_PROVIDERS[provider]["custom_url"]
    elif provider == "azure_openai":
        params.update({
            "api_version": '2024-10-21',
        })
    elif provider == "ollama":
        params["num_ctx"] = 32000
        
    set_llm_environment_variables(provider, LLM_CONFIG["api_key"], LLM_CONFIG.get("endpoint", None))
    
    return LLM_PROVIDERS[provider]["class"](**params)


# Add a function to set the required environment variables for the selected LLM provider
def set_llm_environment_variables(provider, api_key=None, endpoint=None):
    """
    Set the appropriate environment variables for the selected LLM provider.
    This is needed because browser-use now expects these specific environment
    variable names rather than passing them directly to the LLM object.
    """
    
    if provider == "openai":
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            
    elif provider == "deepseek":
        if api_key:
            os.environ["DEEPSEEK_API_KEY"] = api_key
            
    elif provider == "anthropic":
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key
            
    elif provider == "azure_openai":
        if api_key:
            os.environ["AZURE_OPENAI_KEY"] = api_key
        if endpoint:
            os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint
            
    elif provider == "google":
        if api_key:
            print(f"Google API Key is set as {api_key}")
            # Set both environment variables that might be used by browser-use
            os.environ["GOOGLE_API_KEY"] = api_key
            os.environ["GEMINI_API_KEY"] = api_key
            
    logger.info(f"Set environment variables for {provider} provider")

