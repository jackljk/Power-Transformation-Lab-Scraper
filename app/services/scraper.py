import os
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field, ValidationError
import json

# Import browser-use for web scraping with AI
from browser_use import Agent, Controller

from app.models.tasks_models import Task
from app.models.llm_models import get_llm_instance
from app.models.output_format_models import build_output_model
from app.utils.config.browser_use import define_browser_use_context_config
from app.utils.config.agent import RUN_MAX_STEPS, PLANNER_INTERVAL, USE_PLANNER_MODEL
from app.services.scraper_hooks import save_page_content


class WebScraper:
    """
    A web scraper class that uses browser-use to extract targeted information
    from websites based on user prompts.
    """

    def __init__(
        self,
        url: str,
        prompt: Union[str, Dict[str, Any]],
        additional_context: Optional[Dict[str, Any]] = None,
        task_template: str = "default",
        initial_actions: Optional[List[Dict[str, Any]]] = None,
        output_format: Union[BaseModel] = None
    ):
        """
        Initialize the WebScraper.
        """
        assert output_format, "Output format model is required"
        
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
        self.url = url
        self.prompt = prompt
        self.task_template = task_template
        self.output_format = output_format

        # Set the initial actions to go to the URL provided and add from the given
        self.initial_actions = [
            {"open_tab": {"url": url}},
        ] + (initial_actions if initial_actions else [])
        

        # Get the LLM instance for browser-use
        self.llm = get_llm_instance()
        
        self.planner_llm = get_llm_instance(planner=True) if USE_PLANNER_MODEL else None

        # create a browser-use browser config object
        self.browser_context, self.browser_config = define_browser_use_context_config()

        # Create a controller with our output model
        self.controller = Controller(output_model=output_format)

        # Initialize the browser-use agent with the controller
        self.agent = Agent(
            task=task_string, # task string from the task object
            # llm settings
            llm=self.llm,
            planner_llm=self.planner_llm,
            planner_interval=PLANNER_INTERVAL,
            use_vision_for_planner=False,
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

        # build the output model

        if result:
            # Parse the result using our Pydantic model
            try:
                # First try to parse as is (might already be a list)
                parsed: self.output_format = self.output_format.model_validate_json( # type: ignore
                    result
                )
            except ValidationError as e:
                # If direct parsing fails, try wrapping the result in an outputs list
                try:
                    result_obj = json.loads(result)
                    # Wrap the single result in an outputs list
                    wrapped_result = {"outputs": [result_obj]}
                    # Convert back to JSON string
                    result_json = json.dumps(wrapped_result)
                    # Try parsing the wrapped result
                    parsed: self.output_format = self.output_format.model_validate_json( # type: ignore
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

    def _convert_to_scraped_result(self, output):
        """
        Convert the browser-use structured output to our ScrapedResult model.

        Args:
            output: The structured output from browser-use

        Returns:
            A ScrapedResult object with the data from browser-use
        """
        # Extract the relevant data from the output based on our output model structure
        result_dict = output
        if hasattr(output, "model_dump"):
            result_dict = output.model_dump()
        
        # Add metadata to the result
        result_dict["url"] = self.url
        result_dict["prompt"] = self.prompt
        result_dict["task_template"] = self.task_template
        
        return result_dict

    def _create_empty_result(self) -> Dict[str, Any]:
        """
        Create an empty result when no data was returned.

        Returns:
            A dictionary with default values
        """
        empty_result = {
            "content": "",
            "format_type": "text",
            "prompt": self.prompt,
            "url": self.url,
            "summary": "",
        }
        empty_result["task_template"] = self.task_template

        return empty_result
