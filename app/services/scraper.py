import os
from typing import Dict, Any, Optional, List
import json

# Import browser-use for web scraping with AI
from browser_use import Agent, Controller

from app.models.text_models import Citation as TextCitation, ScrapedResult
from app.models.tasks_models import Task
from app.models.output_format_models import ScraperOutput
from app.utils.brower_use import define_browser_use_config
from app.models.llm_models import get_llm_instance
from app.utils.config import RUN_MAX_STEPS


class WebScraper:
    """
    A web scraper class that uses browser-use to extract targeted information
    from websites based on user prompts.
    """
    
    def __init__(self, url: str, prompt: str, additional_context: Optional[Dict[str, Any]] = None, task_template: str = "default"):
        """
        Initialize the WebScraper.
        """
        # Convert additional_context to string format
        additional_context_str = str(additional_context) if additional_context else "None provided"
        
        # Create a Task instance from the specified template
        task_obj = Task.from_template(
            template_name=task_template,
            prompt=prompt,
            additional_context=additional_context_str
        )
        
        # Get the combined task string
        task_string = task_obj.get_combined_task()
        
        # Store task-related properties
        self.task_string = task_string
        self.url = url
        self.prompt = prompt
        self.task_template = task_template
        
        # Get the LLM instance for browser-use
        self.llm = get_llm_instance()
        
        # create a browser-use browser config object
        self.browser_config = define_browser_use_config()
        
        # Create a controller with our output model
        self.controller = Controller(output_model=ScraperOutput)
        
        # Initialize the browser-use agent with the controller
        self.agent = Agent(
            task=task_string,
            llm=self.llm,
            controller=self.controller,
            config=self.browser_config,
        )
    
    async def scrape(self) -> Dict[str, Any]:
        """
        Scrape a website for information based on a prompt.
            
        Returns:
            A structured result containing the extracted information with citations
        """
        # Run the agent to collect information
        history = await self.agent.run(max_steps=RUN_MAX_STEPS)
        
        # Get the final result using the browser-use Controller
        result = history.final_result()
        
        # TODO: ERROR HANDLING/HISTORY Logging
        
        if result:
            # Parse the result using our Pydantic model
            structured_output = ScraperOutput.model_validate_json(result)
            
            # Convert to the application's expected ScrapedResult format
            processed_result = self._convert_to_scraped_result(structured_output)
            
            # Add template info to the result
            result_dict = processed_result.model_dump()
            result_dict["task_template"] = self.task_template
            
            return result_dict
        else:
            # Handle the case where no result was returned
            return self._create_empty_result()
    
    def _convert_to_scraped_result(self, output: ScraperOutput) -> ScrapedResult:
        """
        Convert the browser-use structured output to our ScrapedResult model.
        
        Args:
            output: The structured output from browser-use
            
        Returns:
            A ScrapedResult object with the data from browser-use
        """
        # Convert citations from browser-use format to our application format
        citations = [
            TextCitation(
                text=citation.text,
                source_url=self.url,
                selector_path=citation.location,
                confidence_score=citation.confidence
            )
            for citation in output.citations
        ]
        
        # If no citations were found, add a default citation
        if not citations:
            citations = [
                TextCitation(
                    text="Information extracted from webpage",
                    source_url=self.url,
                    selector_path="",
                    confidence_score=0.7
                )
            ]
        
        # Return the converted result
        return ScrapedResult(
            content=output.content,
            citations=citations,
            format_type=output.format_type,
            prompt=self.prompt,
            url=self.url,
            summary=output.summary
        )
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """
        Create an empty result when no data was returned.
        
        Returns:
            A dictionary with default values
        """
        empty_result = ScrapedResult(
            content="No data extracted",
            citations=[
                TextCitation(
                    text="No information found",
                    source_url=self.url,
                    selector_path="",
                    confidence_score=0.0
                )
            ],
            format_type="text",
            prompt=self.prompt,
            url=self.url
        )
        
        result_dict = empty_result.model_dump()
        result_dict["task_template"] = self.task_template
        
        return result_dict