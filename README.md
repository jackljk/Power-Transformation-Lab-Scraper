# Power Transformation Lab Scraper

An AI-powered web scraper built with browser-use that extracts information from websites based on natural language prompts. This tool ensures accurate information extraction with citations.

## Features

- **Prompt-based Scraping**: Simply provide a URL and describe what information you want to extract
- **Citation Verification**: All extracted information includes citations to verify accuracy
- **Format Flexibility**: Automatically determines the best format for returning extracted data
- **Task Templates**: Multiple task templates for different extraction needs (summary, detailed, Q&A)
- **AI-powered**: Uses browser-use to understand and navigate web pages
- **Configuration System**: Flexible YAML-based configuration system
- **Output Options**: Save results to files or display in console

## Installation

### Prerequisites

- Python 3.11 or higher
- [Playwright](https://playwright.dev/) dependencies for browser automation

### Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd Power-Transformation-Lab-Scraper
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright browsers:
   ```bash
   playwright install chromium
   ```

5. Set up configuration:
   ```bash
   cp app/config/secrets-example.yaml app/config/secrets.yaml
   # Edit secrets.yaml with your API keys and credentials
   ```

## Usage

### Using Configuration Files

The scraper is configured using YAML files in the `app/config` directory:

1. Edit the `app/config/local.yaml` file with your scraping parameters:
   ```yaml
   scraper:
     url: "https://example.com"
     prompt: "Extract information about product pricing"
     output_path: "results/output.json"  # Optional
     task_template: "default"  # Optional (default, summary, detailed, qa)
     context:  # Optional
       format: "json"  
       value: '{"time_period": "last 6 months"}'
   ```

2. Run the scraper:
   ```bash
   python -m app.main
   ```

3. You can also specify an alternative config file:
   ```bash
   python -m app.main my_custom_config.yaml
   ```

### Task Templates

The scraper supports multiple task templates for different extraction needs:

- `default`: General-purpose information extraction with citations
- `summary`: Create a concise summary with key points (WIP)
- `detailed`: Extract comprehensive, hierarchical information (WIP)
- `qa`: Answer questions directly from webpage content (WIP)

### Examples

(WIP)

### Docker Usage

1. Build the Docker image:
   ```bash
   docker build -t power-scraper .
   ```

2. Run the container:
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

## How It Works

The scraper uses browser-use, which combines Playwright browser automation with AI capabilities:

1. The user provides a URL and a prompt describing what information to extract
2. The system loads the URL in a headless browser
3. The AI analyzes the webpage content in relation to the prompt
4. The AI extracts relevant information and provides citations
5. The system processes the AI's response and returns structured data

## Citation Verification

Each piece of extracted information includes:

- The original text from the webpage
- The location where it was found (CSS selector path)
- A confidence score indicating relevance to the prompt

This ensures that the information extracted is 100% verifiable and accurate.

## Configuration System

The scraper uses a hierarchical configuration system:

- `agent_config.yaml`: AI agent configuration
- `browser_config.yaml`: Browser automation settings
- `llm_config.yaml`: Language model parameters
- `local.yaml`: User-specific scraping parameters
- `secrets.yaml`: API keys and credentials (not committed to Git)

### Environment Variables

You can also configure the scraper using environment variables:

- `BROWSER_HEADLESS`: Whether to run the browser in headless mode (default: `true`)
- `BROWSER_TIMEOUT`: Browser timeout in milliseconds (default: `30000`)
- `DEBUG_MODE`: Enable debug logging (default: `false`)

## Project Structure

```
app/
├── config/           # Configuration files
│   ├── agent_config.yaml
│   ├── browser_config.yaml
│   ├── llm_config.yaml
│   ├── local.yaml
│   └── secrets.yaml
├── models/           # Data models
│   ├── llm_models.py
│   ├── output_format_models.py
│   ├── tasks_models.py
│   └── text_models.py
├── services/         # Core functionality
│   └── scraper.py    # Main scraper implementation
├── utils/            # Utility functions
│   ├── brower_use.py
│   ├── config_manager.py
│   ├── config.py
│   └── task_config.py
└── main.py           # Entry point
```

## License

[Specify your license here]