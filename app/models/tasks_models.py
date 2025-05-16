from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union, Type
from app.templates.task_templates import get_task_template, get_available_templates


class Task(BaseModel):
    """Model for defining scraping tasks with customizable formats"""
    task: str = Field(..., description="The task to be performed")
    template_name: str = Field("default", description="Name of the task template used")
    
    @classmethod
    def from_template(cls, prompt: Union[str, Dict[str, Any]], template_name: str = "default",) -> "Task":
        """
        Create a Task instance from a predefined template.
        
        Args:
            template_name: Name of the template to use
            prompt: The prompt to insert into the template
            
        Returns:
            A Task instance with populated task and output_format fields
        """
        template = get_task_template(template_name)
        
        if template_name == "default":
            task_str = template["task_format"].format(
                prompt=prompt,
            )
        elif template_name == "tabular_extraction":
            # handle filter
            if prompt['filters'] is None:
                filter = ""
            else:
                filter = f"5. If filters are available, apply {prompt["filters"]} before extraction"
            
            # handle no_pages
            if prompt["no_pages"] == "all":
                no_pages = "4. If pagination exists, navigate through all pages and extract all data"
            elif isinstance(prompt["no_pages"], int):
                no_pages = f"4. If pagination exists, navigate through at least the first {prompt['no_pages']} pages and extract all data"
            else:
                no_pages = "4. There should be no pagination"
                
            task_str = template["task_format"].format(
                website=prompt["website"],
                data_category=prompt["data_category"],
                data_points=prompt["data_points"],
                no_pages= no_pages,
                filters= filter,
                url=prompt["url"],
            )
        
        
        return cls(
            task=task_str,
            template_name=template_name
        )
    
    def get_task_string(self) -> str:
        """
        Get the complete task string with both the task instructions and output format.
        
        Returns:
            A string combining the task and output format information
        """
        return self.task
    
    @classmethod
    def get_available_templates(cls) -> list:
        """
        Get a list of all available template names.
        
        Returns:
            A list of template names
        """
        return get_available_templates()