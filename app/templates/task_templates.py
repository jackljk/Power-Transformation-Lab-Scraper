"""
Configuration file for defining scraping task templates.
This allows for easy selection of different task formats for the scraper.
"""
from typing import Dict

# Dictionary of predefined task templates
TASK_TEMPLATES = {
    "default": {
        "task_format": """
            From the provided webpage, extract information about: "{prompt}"
            
            Requirements:
            1. The extracted information must be 100% factual and found on the page (DO NOT Infer Data).
            2. For each piece of information, provide a citation with the exact text and location from the webpage.
            3. Provide a location_url to the specific part of the webpage where the information was found.
                - To do this, you can use the following format:
                    - Select a part of the text (e.g., a paragraph, a section, or a phrase) that contains the information or a part of the answer itself.
                    - Use the text selection to create a URL that points to that part of the webpage.
                    - Ensure to use URL-encoding for any special characters in the text selection.
                    - Ensure to use '#:~text=' to indicate the text selection in the URL.
                        - Example: If a part of the text is "This is a sample text", the URL might look like:
                            - https://example.com/page#:~text=This%20is%20a%20sample%20text
            4. Only include information that is relevant to the prompt.

        """
    },  
    "tabular_extraction": {
        "task_format": """
        Extract structured data from {website} about {data_category}.

        1. Navigate to {url}
        2. Identify the table or structured data containing information about {data_points}
        3. Extract all rows and columns while preserving the relationship between data points
        4. If pagination exists, navigate through at least the first {no_pages} pages and extract all data
        5. If filters are available, apply {filters} before extraction

        Format the extracted data in JSON format with appropriate headers following AgentOutput Format. If any data points are missing, mark them as "N/A" rather than leaving them blank.
        """
    }
}

def get_task_template(template_name: str = "default") -> Dict[str, str]:
    """
    Get a task template by name.
    
    Args:
        template_name: The name of the template to retrieve
        
    Returns:
        A dictionary containing the task_format and output_format strings
    """
    return TASK_TEMPLATES.get(template_name, TASK_TEMPLATES["default"])

def get_available_templates() -> list:
    """
    Get a list of all available template names.
    
    Returns:
        A list of template names
    """
    return list(TASK_TEMPLATES.keys())