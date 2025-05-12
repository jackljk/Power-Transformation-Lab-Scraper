import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import json

from app.services.scraper import WebScraper
from app.models.output_format_models import build_output_model


@pytest.fixture
def mock_browser_context():
    """Create a mock browser context for testing."""
    mock_context = MagicMock()
    mock_context.get_page_html = AsyncMock(return_value="<html><body><h1>Test Page</h1></body></html>")
    mock_context.take_screenshot = AsyncMock(return_value="base64encodedscreenshot")
    mock_context.get_current_page = AsyncMock()
    return mock_context


@pytest.fixture
def mock_llm():
    """Create a mock LLM for testing."""
    return MagicMock()


@pytest.fixture
def mock_controller():
    """Create a mock Controller for testing."""
    controller = MagicMock()
    return controller


@pytest.fixture
def mock_agent(mock_browser_context):
    """Create a mock Agent for testing."""
    agent = MagicMock()
    agent.browser_context = mock_browser_context
    
    # Setup history mock
    history_mock = MagicMock()
    history_mock.final_result.return_value = json.dumps({
        "outputs": [
            {
                "content": [{"title": "Test Film", "nominations": 5, "awards_won": 2, "index": 1, "best_picture": True}],
                "citations": [
                    {
                        "source_text": "Test Film won 2 out of 5 nominations",
                        "location": "table.awards",
                        "location_url": "https://example.com#:~:text=Test%20Film%20won%202%20out%20of%205%20nominations"
                    }
                ],
                "format_type": "structured",
                "summary": "Test film data"
            }
        ]
    })
    
    agent.run = AsyncMock(return_value=history_mock)
    return agent


@pytest.mark.asyncio(loop_scope="session")
async def test_scraper_init():
    """Test WebScraper initialization."""
    with patch('app.services.scraper.get_llm_instance') as mock_get_llm:
        with patch('app.services.scraper.define_browser_use_context_config') as mock_define_config:
            with patch('app.services.scraper.Controller') as mock_controller_class:
                with patch('app.services.scraper.Agent') as mock_agent_class:
                    with patch('app.models.output_format_models') as mock_output_model:
                        # Setup mocks
                        mock_get_llm.return_value = MagicMock()
                        mock_define_config.return_value = (MagicMock(), MagicMock())
                        mock_controller_class.return_value = MagicMock()
                        
                        # Create a mock output model
                        from pydantic import BaseModel
                        from typing import List, Optional
                        
                        class TestContentModel(BaseModel):
                            title: str
                            nominations: int
                            awards_won: int
                            
                        class TestOutputModel(BaseModel):
                            content: List[TestContentModel]
                            format_type: str = "structured"
                            summary: Optional[str] = None
                        
                        mock_output_model.return_value = TestOutputModel
                        
                        # Initialize scraper
                        scraper = WebScraper(
                            url="https://example.com",
                            prompt="Extract film information",
                            task_template="default",
                            output_format=TestOutputModel
                        )
                        
                        # Verify initialization
                        assert scraper.url == "https://example.com"
                        assert scraper.prompt == "Extract film information"
                        assert scraper.task_template == "default"
                        assert scraper.initial_actions[0] == {"open_tab": {"url": "https://example.com"}}
                        assert mock_agent_class.called


# @pytest.mark.asyncio
# async def test_scraper_scrape():
#     """Test WebScraper.scrape method."""
#     with patch('app.services.scraper.get_llm_instance'):
#         with patch('app.services.scraper.define_browser_use_context_config', return_value=(MagicMock(), MagicMock())):
#             with patch('app.services.scraper.Controller'):
#                 with patch('app.services.scraper.Agent') as mock_agent_class:
                        
                        
#                         test_content_model_structure = {
#                             'test_model_content': {
#                                 "title": 'str',
#                                 "nominations": 'int',
#                                 "awards_won": 'int',
#                                 "index": 'int',
#                                 "best_picture": 'bool'
#                             }
#                         }
                        
#                         output_format = build_output_model(test_content_model_structure)

                        
#                         # Setup agent mock
#                         mock_agent = MagicMock()
                        
#                         # Setup history mock
#                         history_mock = MagicMock()
#                         mock_content = {
#                             'title':"Test Film",
#                             'nominations':5,
#                             'awards_won':2,
#                             'index':1,
#                             'best_picture':True
#                         }
#                         history_mock.final_result.return_value = json.dumps({
#                             "outputs": [
#                                 {
#                                     "content": [mock_content],
#                                     "format_type": "structured",
#                                     "summary": "Test film data"
#                                 }
#                             ]
#                         })
                        
#                         mock_agent.run = AsyncMock(return_value=history_mock)
#                         mock_agent_class.return_value = mock_agent
                        
#                         # Initialize scraper
#                         scraper = WebScraper(
#                             url="https://example.com",
#                             prompt="Extract film information",
#                             task_template="default",
#                             output_format=output_format
#                         )
                        
#                         # Call scrape method
#                         result = await scraper.scrape()
                        
#                         # Verify result
#                         assert isinstance(result, dict)
#                         assert "task_template" in result
#                         assert "prompt" in result
#                         assert "outputs" in result
#                         assert len(result["outputs"]) == 1
#                         assert result["outputs"][0]["content"][0]["title"] == "Test Film"
#                         assert result["outputs"][0]["content"][0]["nominations"] == 5
#                         assert mock_agent.run.called