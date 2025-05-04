import pytest
import asyncio
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
import json

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup asyncio for pytest
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# Mock environment variables for testing
@pytest.fixture(scope="function")
def mock_env_variables():
    """Set up mock environment variables for testing."""
    # Save original environment
    original_env = os.environ.copy()
    
    # Set test environment variables
    os.environ["RESULTS_PATH"] = "/tmp/test_results"
    os.environ["PROFILE_PATH"] = "/tmp/test_profile"
    os.environ["OPENAI_API_KEY"] = "test_openai_key"
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

# Create test directories
@pytest.fixture(scope="function")
def test_directories():
    """Create test directories for results, etc."""
    # Create test directories
    os.makedirs("/tmp/test_results", exist_ok=True)
    os.makedirs("/tmp/test_results/local", exist_ok=True)
    os.makedirs("/tmp/test_results/trace", exist_ok=True)
    
    yield
    
    # Cleanup is optional for temporary directories

# Mock browser context
@pytest.fixture
def mock_browser_context():
    """Create a mock browser context for testing."""
    mock_context = MagicMock()
    mock_context.get_page_html = AsyncMock(return_value="<html><body><h1>Test Page</h1></body></html>")
    mock_context.take_screenshot = AsyncMock(return_value="base64encodedscreenshot")
    mock_context.get_current_page = AsyncMock(return_value="https://example.com")
    mock_context.get_current_url = AsyncMock(return_value="https://example.com")
    mock_context.click = AsyncMock()
    mock_context.type = AsyncMock()
    mock_context.navigate = AsyncMock()
    return mock_context

# Mock LLM client
@pytest.fixture
def mock_llm():
    """Create a mock LLM client for testing."""
    mock = MagicMock()
    mock.completion = AsyncMock(return_value="Test completion response")
    mock.chat_completion = AsyncMock(return_value={
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "outputs": [
                            {
                                "content": "Test content",
                                "citations": [
                                    {
                                        "source_text": "Test citation",
                                        "location": "div.content",
                                        "location_url": "https://example.com#citation"
                                    }
                                ],
                                "format_type": "text",
                                "summary": "Test summary"
                            }
                        ]
                    })
                }
            }
        ]
    })
    return mock

# Mock config manager
@pytest.fixture
def mock_config_manager():
    """Create a mock ConfigManager for testing."""
    mock = MagicMock()
    mock.get.side_effect = lambda key, default=None: {
        "llm_config.model": "gpt-4",
        "llm_config.temperature": 0.7,
        "browser_config.headless": True,
        "browser_config.timeout": 30000,
        "agent_config.max_steps": 10
    }.get(key, default)
    
    mock.get_secret.return_value = "test_secret_value"
    return mock

# Mock for the scraper agent
@pytest.fixture
def mock_agent():
    """Create a mock Agent for testing."""
    agent = MagicMock()
    
    # Setup history mock
    history_mock = MagicMock()
    history_mock.final_result.return_value = json.dumps({
        "outputs": [
            {
                "content": "Extracted test content",
                "citations": [
                    {
                        "source_text": "Test source text",
                        "location": "div.content",
                        "location_url": "https://example.com#citation"
                    }
                ],
                "format_type": "text",
                "summary": "Test summary"
            }
        ]
    })
    
    agent.run = AsyncMock(return_value=history_mock)
    return agent