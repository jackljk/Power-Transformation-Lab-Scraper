from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List, Union, Type
from app.utils.task_config import get_task_template, get_available_templates


class Task(BaseModel):
    """Model for defining scraping tasks with customizable formats"""
    task: str = Field(..., description="The task to be performed")
    output_format: Union[str, Type[BaseModel]] = Field(
        ..., 
        description="The format of the output (string instructions or Pydantic model)"
    )
    template_name: str = Field("default", description="Name of the task template used")
    
    @classmethod
    def from_template(cls, template_name: str = "default", prompt: str = "", additional_context: str = "None provided") -> "Task":
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
            additional_context=additional_context
        )
        
        output_format = template["output_format"]
        
        return cls(
            task=task_str,
            output_format=output_format,
            template_name=template_name
        )
    
    def get_combined_task(self) -> str:
        """
        Get the complete task string with both the task instructions and output format.
        
        Returns:
            A string combining the task and output format information
        """
        # If output_format is a Pydantic model class, use its schema
        if isinstance(self.output_format, type) and issubclass(self.output_format, BaseModel):
            schema = self.output_format.model_json_schema()
            # Create a simplified format instruction based on the model schema
            format_instructions = (
                f"Return your response as a JSON object that matches this schema:\n"
                f"{schema.get('title', 'OutputFormat')} with fields:\n"
            )
            
            # Add descriptions for each required property
            required = schema.get('required', [])
            properties = schema.get('properties', {})
            
            for prop_name, prop_info in properties.items():
                desc = prop_info.get('description', 'No description')
                is_required = prop_name in required
                format_instructions += f"- {prop_name}: {desc}{' (required)' if is_required else ''}\n"
                
            return f"{self.task}\n\n{format_instructions}"
        else:
            # If it's a string, use it directly
            return f"{self.task}\n\n{self.output_format}"
    
    @classmethod
    def get_available_templates(cls) -> list:
        """
        Get a list of all available template names.
        
        Returns:
            A list of template names
        """
        return get_available_templates()