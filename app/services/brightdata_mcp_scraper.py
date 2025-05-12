from typing import Dict, Any, Optional, Union

from app.models.tasks_models import Task
from app.models.llm_models import get_llm_instance
from app.utils.config.brightdata_mcp import define_mcp_server_params
from app.templates.mcp_rule_templates import MCP_TEMPLATES  

from mcp import ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
import json

class BrightDataMCPScraper:
    """
    This class is responsible for scraping the Bright Data MCP (Managed Crawling Platform) for proxy information.
    """

    def __init__(
        self,
        url: str,
        prompt: str,
        task_template: str = "default",
        additional_context: Optional[Dict[str, Any]] = None,
        output_format: Union[Dict[str, Any]] = None,
    ):
        """
        Initialize the BrightDataMCPScraper.
        Args:
            url: The URL to scrape.
            prompt: The prompt for the scraping task.
            additional_context: Optional additional context to help with scraping.
            output_format: The format of the output data.
        """
        assert output_format, "Output format model is required"
        assert url, "URL is required"
        
        # Convert additional_context to string format
        additional_context_str = (
            str(additional_context) if additional_context else "None provided"
        )
        
        # Create a Task instance from the specified template
        task_string = Task.from_template(
            template_name=task_template,
            prompt=prompt,
        ).get_task_string()        
        
        # Store task-related properties
        self.task_string = task_string
        self.additional_context = additional_context_str
        self.url = url
        self.prompt = prompt
        self.task_template = task_template
        self.output_format = json.dumps(output_format, indent=4)
        
        # Get the LLM instance for mcp scraping
        self.llm = get_llm_instance()
        
        # get the mcp server parameters
        self.server_params = define_mcp_server_params()

        # init the content for the MCP scraper
        self._init_content()

    async def scrape(self) -> Dict[str, Any]:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Load the tools for the MCP agent
                tools = await load_mcp_tools(session)
                
                # Create the MCP agent
                agent = create_react_agent(
                    self.llm, tools
                )
                
                messages = [
                    {
                        "role": "system",
                        'content': MCP_TEMPLATES["default"]
                    },
                    {
                        "role": "user",
                        'content': self.content
                    },
                ]
                
                # Run the agent with the task string and URL
                response = await agent.ainvoke({
                    'messages': messages,
                })
                
                
                return response

    def _init_content(self):
        """
        Initialize the content for the MCP scraper.
        - Combines the prompts, url, and additional context into a single string.
        - This string is used to create the task/message for the MCP agent.
        """
        self.content = f"""
        URL: {self.url}
        Prompt: {self.prompt}
        Additional content: {self.additional_context}
        Output format: {self.output_format}
        """
        