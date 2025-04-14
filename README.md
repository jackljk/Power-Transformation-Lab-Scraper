# Power Transformation Lab Scraper

An AI-powered web scraper built with browser-use that extracts information from websites based on natural language prompts. This tool ensures accurate information extraction with citations.

## Features

- **Prompt-based Scraping**: Simply provide a URL and describe what information you want to extract
- **Citation Verification**: All extracted information includes citations to verify accuracy
- **Format Flexibility**: Automatically determines the best format for returning extracted data
- **Task Templates**: Multiple task templates for different extraction needs (summary, detailed, Q&A)
- **AI-powered**: Uses browser-use to understand and navigate web pages
- **Command-line Interface**: Easy-to-use CLI for quick scraping tasks

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

5. Create a `.env` file based on the provided `.env.example`:
   ```bash
   cp .env.example .env
   ```

## Usage

### Command-line Interface

The scraper can be run from the command line:

```bash
python -m app.main --url "https://example.com" --prompt "Extract information about product pricing"
```

#### Command-line Options

- `--url` or `-u`: The URL to scrape (required)
- `--prompt` or `-p`: The information to extract (required)
- `--context` or `-c`: Additional context to help guide the extraction (optional, can be JSON)
- `--output` or `-o`: Output file path (optional, defaults to console output)
- `--template` or `-t`: Task template to use (optional, defaults to "default")

### Task Templates

The scraper supports multiple task templates for different extraction needs:

- `default`: General-purpose information extraction with citations
- `summary`: Create a concise summary with key points
- `detailed`: Extract comprehensive, hierarchical information
- `qa`: Answer questions directly from webpage content

Example using a specific template:
```bash
python -m app.main --url "https://example.com/about" --prompt "What is the company's mission?" --template "qa"
```

### Examples

Extract product pricing information and print to console:
```bash
python -m app.main --url "https://example.com/products" --prompt "Extract all product prices and their names"
```

Extract company information and save to a file:
```bash
python -m app.main --url "https://example.com/about" --prompt "Extract company history and key milestones" --output "company_info.json"
```

Provide additional context for better extraction:
```bash
python -m app.main --url "https://example.com/blog" --prompt "Find articles about machine learning" --context '{"time_period": "last 6 months", "focus_area": "computer vision"}'
```

### Docker Usage

1. Build the Docker image:
   ```bash
   docker build -t power-scraper .
   ```

2. Run the container:
   ```bash
   docker run --env-file .env power-scraper --url "https://example.com" --prompt "Extract product information"
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

## Configuration

You can configure the scraper using environment variables in the `.env` file:

- `BROWSER_HEADLESS`: Whether to run the browser in headless mode (default: `true`)
- `BROWSER_TIMEOUT`: Browser timeout in milliseconds (default: `30000`)
- `DEBUG_MODE`: Enable debug logging (default: `false`)

## License

[Specify your license here]