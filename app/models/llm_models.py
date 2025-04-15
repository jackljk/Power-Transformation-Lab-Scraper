from typing import Any
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic

from utils.config import get_llm_config

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
    
    # Provider-specific configurations
    if provider != "ollama":
        params["api_key"] = LLM_CONFIG.get("api_key")
    
    if provider == "azure_openai":
        params.update({
            "api_version": '2024-10-21',
            "azure_endpoint": LLM_CONFIG.get("endpoint"),
        })
    elif provider == "ollama":
        params["num_ctx"] = 32000
    elif provider == "deepseek":
        params["base_url"] = LLM_PROVIDERS[provider]["custom_url"]
    
    return LLM_PROVIDERS[provider]["class"](**params)
