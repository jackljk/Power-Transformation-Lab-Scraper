from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union, Type
from utils.task_config import get_task_template, get_available_templates


class Task(BaseModel):
    """Model for defining scraping tasks with customizable formats"""
    task: str = Field(..., description="The task to be performed")
    template_name: str = Field("default", description="Name of the task template used")
    
    @classmethod
    def from_template(cls, template_name: str = "default", prompt: str = "") -> "Task":
        """
        Create a Task instance from a predefined template.
        
        Args:
            template_name: Name of the template to use
            prompt: The prompt to insert into the template
            additional_context: Additional context to insert into the template
            
        Returns:
            A Task instance with populated task and output_format fields
        """
        template = get_task_template(template_name)
        
        task_str = template["task_format"].format(
            prompt=prompt,
        )
        
        return cls(
            task=task_str,
            template_name=template_name
        )
    
    def get_combined_task(self) -> str:
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