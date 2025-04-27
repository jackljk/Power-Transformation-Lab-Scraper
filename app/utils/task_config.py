"""
Configuration file for defining scraping task templates.
This allows for easy selection of different task formats for the scraper.
"""
from typing import Dict, Any

# Dictionary of predefined task templates
TASK_TEMPLATES = {
    "default": {
        "task_format": """
            From the provided webpage, extract information about: "{prompt}"
            
            Requirements:
            1. The extracted information must be 100% factual and found on the page.
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
    
    "summary": {
        "task_format": """
            From the provided webpage, create a concise summary about: "{prompt}"
            
            Requirements:
            1. Focus on creating a brief, easy-to-understand summary.
            2. Include only the most important facts related to the prompt.
            3. Aim for 3-5 key points that address the core of the prompt.
            4. For each key point, provide a citation with the exact text from the webpage.
            
            Additional context: {additional_context}
        """,
        "output_format": """
            Format the output as a JSON with the following structure:
            {{
                "summary": "A concise 1-2 paragraph summary addressing the prompt",
                "key_points": [
                    "First key point about the topic",
                    "Second key point about the topic",
                    "Third key point about the topic"
                ],
                "citations": [
                    {{
                        "text": "exact text from webpage",
                        "location": "description of where this was found",
                        "confidence": 0.95
                    }}
                ]
            }}
        """
    },
    
    "detailed": {
        "task_format": """
            From the provided webpage, extract comprehensive and detailed information about: "{prompt}"
            
            Requirements:
            1. Extract all relevant information on the page related to the prompt.
            2. Organize the information in a hierarchical structure with main topics and subtopics.
            3. Include numerical data, dates, and specific details where available.
            4. For each piece of information, provide a citation with the exact text and location.
            5. Include context to help understand the significance of the information.
            
            Additional context: {additional_context}
        """,
        "output_format": """
            Format the output as a JSON with the following structure:
            {{
                "main_topics": [
                    {{
                        "title": "Topic Title",
                        "content": "Detailed explanation",
                        "subtopics": [
                            {{
                                "title": "Subtopic Title",
                                "content": "Detailed explanation"
                            }}
                        ]
                    }}
                ],
                "key_data_points": [
                    {{
                        "label": "Data point name",
                        "value": "Data point value",
                        "context": "Why this matters"
                    }}
                ],
                "citations": [
                    {{
                        "text": "exact text from webpage",
                        "location": "description of where this was found",
                        "confidence": 0.95
                    }}
                ],
                "format_type": "detailed"
            }}
        """
    },
    
    "qa": {
        "task_format": """
            From the provided webpage, answer questions about: "{prompt}"
            
            Requirements:
            1. Treat the prompt as a question that needs a direct answer.
            2. Provide a clear, concise answer based only on information from the webpage.
            3. If the question cannot be answered from the webpage content, clearly state this.
            4. Include quotes from the webpage that support your answer.
            5. Provide confidence levels for your answer.
            
            Additional context: {additional_context}
        """,
        "output_format": """
            Format the output as a JSON with the following structure:
            {{
                "question": "The original question from the prompt",
                "answer": "Direct answer to the question",
                "supporting_evidence": [
                    "Quote from the webpage that supports the answer",
                    "Another relevant quote"
                ],
                "confidence_level": 0.95,
                "citations": [
                    {{
                        "text": "exact text from webpage",
                        "location": "description of where this was found"
                    }}
                ]
            }}
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