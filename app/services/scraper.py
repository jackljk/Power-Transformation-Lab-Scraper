import os
from typing import Dict, Any, Optional, List
import json

# Import browser-use for web scraping with AI
from browser_use import Agent, Controller

from models.text_models import Citation as TextCitation, ScrapedResult
from models.tasks_models import Task
from models.llm_models import get_llm_instance
from models.output_format_models import ScraperOutput, ScraperOutputList
from app.utils.config.browser_use import define_browser_use_context_config
from utils.config.agent import RUN_MAX_STEPS, PLANNER_INTERVAL, USE_PLANNER_MODEL
from services.scraper_hooks import save_page_content

class WebScraper:
    """
    A web scraper class that uses browser-use to extract targeted information
    from websites based on user prompts.
    """

    def __init__(
        self,
        url: str,
        prompt: str,
        additional_context: Optional[Dict[str, Any]] = None,
        task_template: str = "default",
        initial_actions: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Initialize the WebScraper.
        """
        # Convert additional_context to string format
        additional_context_str = (
            str(additional_context) if additional_context else "None provided"
        )

        # Create a Task instance from the specified template
        task_obj = Task.from_template(
            template_name=task_template,
            prompt=prompt,
        )

        # Get the combined task string
        task_string = task_obj.get_combined_task()

        # Store task-related properties
        self.task_string = task_string
        self.url = url
        self.prompt = prompt
        self.task_template = task_template

        # Set the initial actions to go to the URL provided and add from the given
        self.initial_actions = [
            {"open_tab": {"url": url}},
        ] + (initial_actions if initial_actions else [])
        

        # Get the LLM instance for browser-use
        self.llm = get_llm_instance()
        
        # self.planner_llm = get_planner_llm_instance()

        # create a browser-use browser config object
        self.browser_context, self.browser_config = define_browser_use_context_config()

        # Create a controller with our output model
        self.controller = Controller(output_model=ScraperOutput)

        # Initialize the browser-use agent with the controller
        self.agent = Agent(
            task=task_string, # task string from the task object
            # llm settings
            llm=self.llm,
            planner_llm=self.planner_llm,
            planner_interval=PLANNER_INTERVAL,
            # Model output controller
            controller=self.controller,
            # Additional context/initial actions
            message_context=additional_context_str,
            initial_actions=self.initial_actions,
            # browser-use config
            browser_context=self.browser_context,
        )

    async def scrape(self) -> Dict[str, Any]:
        """
        Scrape a website for information based on a prompt.

        Returns:
            A structured result containing the extracted information with citations
        """
        # Run the agent to collect information
        history = await self.agent.run(max_steps=RUN_MAX_STEPS, on_step_end=save_page_content)

        # Get the final result using the browser-use Controller
        result = history.final_result()

        # TODO: ERROR HANDLING/HISTORY Logging

        if result:
            # Parse the result using our Pydantic model
            try:
                # First try to parse as is (might already be a list)
                parsed: ScraperOutputList = ScraperOutputList.model_validate_json(
                    result
                )
            except Exception as e:
                # If direct parsing fails, try wrapping the result in an outputs list
                try:
                    result_obj = json.loads(result)
                    # Wrap the single result in an outputs list
                    wrapped_result = {"outputs": [result_obj]}
                    # Convert back to JSON string
                    result_json = json.dumps(wrapped_result)
                    # Try parsing the wrapped result
                    parsed: ScraperOutputList = ScraperOutputList.model_validate_json(
                        result_json
                    )
                except Exception:
                    # If both approaches fail, raise the original error
                    raise e

            # add json to result_dict
            result_dict = parsed.model_dump()

            # add template information to result_dict
            result_dict["task_template"] = self.task_template

            # Add prompt and URL to the result_dict
            result_dict["prompt"] = self.prompt

            # Convert to the application's expected ScrapedResult format
            # processed_result = self._convert_to_scraped_result(structured_output)

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
                confidence_score=citation.confidence,
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
                    confidence_score=0.7,
                )
            ]

        # Return the converted result
        return ScrapedResult(
            content=output.content,
            citations=citations,
            format_type=output.format_type,
            prompt=self.prompt,
            url=self.url,
            summary=output.summary,
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
                    confidence_score=0.0,
                )
            ],
            format_type="text",
            prompt=self.prompt,
            url=self.url,
        )

        result_dict = empty_result.model_dump()
        result_dict["task_template"] = self.task_template

        return result_dict
