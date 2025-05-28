# Power Transformation Lab Scraper

An AI-powered multi-scraper system that extracts information from websites and documents based on natural language prompts. This tool combines multiple scraping technologies to ensure accurate information extraction with citations and structured output.

## Features

- **Multiple Scraper Technologies**: Support for browser automation, proxy-based scraping, and PDF document processing
- **Prompt-based Extraction**: Simply provide a URL/document and describe what information you want to extract
- **Format Flexibility**: Custom-defined output formats for your specific data needs
- **Task Templates**: Multiple task templates for different extraction needs (default, tabular, PDF)
- **Profile System**: Reusable configuration profiles for common scraping tasks
- **Local Tracing**: Detailed logging and screenshot captures for debugging and verification

## Scraper Types

The system supports three primary methods of data extraction, each optimized for different use cases:

### Browser-Use Scraper

Uses browser automation with AI capabilities to interact with websites as a human would:
- **Technology**: Playwright + AI-powered navigation
- **Best for**: Complex websites requiring interaction, JavaScript-heavy sites, dynamic content
- **Features**: 
  - Full browser rendering with JavaScript support
  - AI-powered navigation and interaction
  - Screenshot capturing for verification
  - Support for complex user flows (clicks, scrolls, form filling)
- **Use cases**: Interactive (Reactive) sites, unstructured data
### Bright Data MCP Scraper

Uses Bright Data's Managed Crawling Platform for proxy-based scraping:
- **Technology**: Bright Data proxy network + LangGraph agents
- **Best for**: Large-scale scraping, sites with anti-bot protection, fast data collection
- **Features**:
  - Built-in proxy rotation to avoid blocking
  - Headless execution for faster scraping
  - Residential and datacenter proxy support
  - Global IP rotation
- **Use cases**: Site with blockers, Reactive site

### PDF Scraper

Extracts information from PDF documents using advanced text processing:
- **Technology**: PyMuPDF + OpenAI embeddings + vector search
- **Best for**: Academic papers, reports, documentation, structured documents
- **Features**:
  - Support for single or multiple PDF files
  - Conversion of PDFs to markdown for processing
  - Chunking for large documents to optimize extraction
  - Vector-based retrieval for optimal information finding
  - Support for complex document structures
- **Use cases**: Research papers, financial reports, technical documentation, basically PDFs

## Environment Setup

### Prerequisites

- Python 3.11 or higher
- [Playwright](https://playwright.dev/) dependencies for browser automation (Browser-Use scraper)
- OpenAI API key (for AI processing)
   - Or any of your choice. `see config/secrets-example.yaml`
- Bright Data account and credentials (for Bright Data MCP scraper)

### Installation Steps

1. **Clone the repository:**
   ```powershell
   git clone [repository-url]
   cd Power-Transformation-Lab-Scraper
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers (for Browser-Use scraper):**
   ```powershell
   playwright install chromium
   ```

4. **Configure secrets:**
   ```powershell
   # Copy the example secrets file
   copy app\config\secrets-example.yaml app\config\secrets.yaml
   
   # Edit secrets.yaml with your API keys and credentials
   app\config\secrets.yaml
   ```

   Required configurations in `secrets.yaml`:
   ```yaml
   openai: # For all scraping
     api_key: "your-openai-api-key"
   
   bright_data: # only for bright data MCP scraper
     username: "your-bright-data-username"
     password: "your-bright-data-password"
   ```
    More AI options avaliable - see `config/secrets-example.yaml`
## How to Run the Scraper

### Method 1: Using Profile Configuration (Recommended)

1. **Create or select a profile** in `app/config/profiles/` (see Profile Creation section)

2. **Configure the profile to use** in `app/config/local.yaml`:
   ```yaml
   profile: "your_profile_name"
   ```

3. **Run the scraper:**
   ```powershell
   python main.py
   ```

### Method 2: Command Line Arguments

Run the scraper with a specific profile:
```powershell
python main.py --profile=profile_name
```


## Profile Creation

Profiles are YAML configuration files that define what to scrape and how to format the output. They provide a reusable way to configure scraping tasks.

### Creating a New Profile

1. **Create a new YAML file** in `app/config/profiles/` (e.g., `my_scraper.yaml`)

2. **Basic Profile Structure:**
   ```yaml
   # Name for profile (for logs/results identification)
   name: "my_scraper_profile"
   
   scraper:
     # Choose scraper type
     scraper_type: "browser_use"  # "browser_use", "bright_data_mcp", or "pdf_scraper"
     
     # For web scraping
     url: "https://example.com"
     
     # OR for PDF scraping
     # filepath: "data/document.pdf"
     # filepath: ["data/doc1.pdf", "data/doc2.pdf"]  # Multiple PDFs
     
     # Information to extract
     prompt: 
       task_template: "default"  # "default", "tabular_extraction", "pdf_default"
       text: "Extract information about X, Y, and Z"
     
     # Additional context (optional)
     additional_context:
       format: "text"
       value: "Additional guidance for the scraper"
     
     # Initial actions for browser automation (optional, browser_use only)
     initial_actions:
       - scroll_down: 400
       - wait: 2000
       # - go_to_url: "https://example.com/subpage"
   
   # Define the structure of output data
   content_structure:
     DataType:
       field1: str
       field2: int
       field3: bool
   ```

3. **Configure your local.yaml** to use the profile:
   ```yaml
   profile: "my_scraper_profile"
   ```

### Profile Configuration Reference

For detailed information about all available profile configuration options, see [`docs/profile-configuration.md`](docs/profile-configuration.md).

## Local Tracing and Results

The scraper maintains detailed logs and artifacts of its operation for debugging and verification purposes.

### Results Directory Structure

Results are automatically saved in the `results/` directory with the following structure:

```
results/
├── profile_name/
│   ├── timestamp_folder/
│   │   ├── output.json           # Final extracted data
│   │   ├── trace.json            # Detailed trace of operations
│   │   ├── screenshots/          # Screenshots during execution
│   │   │   ├── step-1.png
│   │   │   ├── step-2.png
│   │   │   └── ...
│   │   └── webpage-1/            # Page-specific data (browser_use)
│   │       └── webpage-1.pdf     # PDF snapshot of the page
```

**WIP** - The verboseness of the tracing can be configured in `local.yaml`

<!-- TODO -->
<!-- ### Understanding Trace Files

The `trace.json` file contains comprehensive information about the scraping process:

```json
{
  "execution_id": "unique-execution-id",
  "start_time": "2025-05-25T15:30:00Z",
  "scraper_type": "browser_use",
  "steps": [
    {
      "step_number": 1,
      "action": "navigate_to_url",
      "url": "https://example.com",
      "screenshot": "screenshots/step-1.png",
      "timestamp": "2025-05-25T15:30:05Z"
    },
    {
      "step_number": 2,
      "action": "extract_data",
      "extracted_elements": 15,
      "screenshot": "screenshots/step-2.png",
      "timestamp": "2025-05-25T15:30:10Z"
    }
  ],
  "final_result": { "extracted_data": "..." },
  "errors": [],
  "total_execution_time": "45.2s"
}
```

### Debugging with Traces

- **Screenshots**: Visual record of each step for debugging navigation issues
- **Action History**: Complete log of all actions performed by the scraper
- **Error Tracking**: Detailed error messages with context
- **Performance Metrics**: Execution time for each step and overall process -->

## Task Templates

The scraper supports different task templates optimized for specific extraction scenarios:

### Available Templates

1. **`default`**: General-purpose information extraction
   - Best for: Most web scraping tasks
   - Features: Flexible extraction 

2. **`tabular_extraction`**: Optimized prompting for structured data extraction
   - Best for: Tables, lists, structured data
   - Features: Better preserves data relationships

3. **`pdf_default`**: Optimized for PDF document processing - use for pdfs

### Custom Task Templates

You can create custom task templates by modifying `app/templates/task_templates.py`. See [`docs/custom-templates.md`](docs/custom-templates.md) for detailed instructions.

## Browser Actions (Browser-Use Scraper)

For the browser-use scraper, you can define initial actions to perform before extraction:

```yaml
initial_actions:
  - scroll_down: 500        # Scroll down 500 pixels
  - scroll_up: 300          # Scroll up 300 pixels
  - wait: 2000              # Wait 2 seconds
  - go_to_url: "https://example.com/subpage"  # Navigate to another page
  - click_by_xpath: "//button[@id='load-more']"  # Click specific element
```

Available actions:
- `scroll_down: <pixels>`: Scroll down by specified pixels
- `scroll_up: <pixels>`: Scroll up by specified pixels
- `go_to_url: <url>`: Navigate to a specific URL
- `wait: <milliseconds>`: Wait for specified duration
- `click_by_xpath: <xpath>`: Click element by XPath selector

## Configuration System

The scraper uses a hierarchical configuration system with multiple YAML files:

### Configuration Files

- **`app/config/local.yaml`**: Main configuration file for scraping parameters
- **`app/config/profiles/`**: Directory containing reusable profile configurations
- **`app/config/secrets.yaml`**: API keys and credentials (not committed to Git)
- **`app/config/agent_config.yaml`**: AI agent configuration
- **`app/config/browser_config.yaml`**: Browser automation settings
- **`app/config/llm_config.yaml`**: Language model parameters
- **`app/config/mcp_config.yaml`**: Bright Data MCP configuration

### Environment Variables

You can also configure the scraper using environment variables:

- `BROWSER_HEADLESS`: Whether to run browser in headless mode (default: `true`)
- `BROWSER_TIMEOUT`: Browser timeout in milliseconds (default: `30000`)
- `DEBUG_MODE`: Enable debug logging (default: `false`)
- `OPENAI_API_KEY`: OpenAI API key
- `RUN_MAX_STEPS`: Maximum steps for browser automation (default: `50`)

## Troubleshooting

For detailed troubleshooting information, see [`docs/troubleshooting.md`](docs/troubleshooting.md).

### Quick Fixes

- **Playwright issues**: Run `playwright install chromium`
- **API key errors**: Check `app/config/secrets.yaml`
- **PDF extraction issues**: Ensure PDFs are text-based, not scanned images
- **Memory issues**: Enable headless mode and reduce browser steps

### Debug Mode (WIP)
<!-- 
Enable detailed logging for troubleshooting:

```powershell
$env:DEBUG_MODE = "true"
python main.py
```

Debug mode provides:
- Detailed step-by-step logs
- Screenshot captures at each step
- Network request/response logs
- Performance timing information -->

### Known Bugs
- **Windows asyncio errors**


### Getting Help

1. Check the `trace.json` file in your results directory for detailed execution logs
2. Review screenshots in the results directory to understand navigation issues
3. Enable debug mode for more detailed logging
4. Check the examples in the `examples/` directory for reference configurations
5. See [`docs/troubleshooting.md`](docs/troubleshooting.md) for comprehensive troubleshooting

## Examples

Example configurations and use cases can be found in the [`examples/`](examples/) directory. These include:

- Web scraping examples for different site types
- PDF extraction examples for various document formats
- Complex multi-step scraping workflows
- Custom output format examples

## Project Structure

```
Power-Transformation-Lab-Scraper/
├── app/
│   ├── config/                    # Configuration files
│   │   ├── profiles/              # Scraping profile configurations
│   │   ├── agent_config.yaml      # AI agent settings
│   │   ├── browser_config.yaml    # Browser automation settings
│   │   ├── llm_config.yaml        # Language model configuration
│   │   ├── local.yaml             # Main configuration file
│   │   ├── mcp_config.yaml        # Bright Data MCP settings
│   │   └── secrets.yaml           # API keys and credentials
│   ├── models/                    # Data models and schemas
│   │   ├── llm_models.py          # Language model configurations
│   │   ├── output_format_models.py # Output format definitions
│   │   └── tasks_models.py        # Task model definitions
│   ├── services/                  # Core scraping services
│   │   ├── browser_use_scraper.py # Browser automation scraper
│   │   ├── brightdata_mcp_scraper.py # Bright Data MCP scraper
│   │   ├── pdf_scraper.py         # PDF document scraper
│   │   └── hooks/                 # Scraper event hooks
│   ├── templates/                 # Task and prompt templates
│   │   ├── task_templates.py      # Predefined task templates
│   │   └── mcp_rule_templates.py  # MCP-specific templates
│   └── utils/                     # Utility functions
│       ├── config_manager.py      # Configuration management
│       ├── logging.py             # Logging utilities
│       ├── scraper_utils.py       # Scraper helper functions
│       └── config/                # Configuration utilities
├── docs/                          # Documentation
├── examples/                      # Example configurations and use cases
├── data/                          # Input data files (PDFs, etc.)
├── results/                       # Scraping results and traces
├── main.py                        # Main entry point
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Examples and Use Cases

The `examples/` directory contains comprehensive example profiles for various scraping scenarios:

### Quick Start Examples
- **E-commerce**: Amazon product extraction, eBay auction monitoring
- **News**: BBC article extraction, Reuters breaking news monitoring
- **Finance**: Yahoo Finance data tables, annual report analysis
- **Social Media**: LinkedIn company profiles, Twitter trend monitoring
- **Academic**: Research paper analysis, technical documentation extraction

### Advanced Examples
- **Multi-scraper Workflows**: Company research pipeline, market analysis
- **High-Performance**: Large-scale news aggregation, enterprise monitoring
- **Security**: Secure document processing with PII protection

### Getting Started
1. Browse examples in `examples/` directory
2. See `examples/PROFILE-SELECTION-GUIDE.md` for choosing the right profile
3. Read `examples/USAGE.md` for detailed customization instructions
4. Copy and modify profiles for your specific needs

```powershell
# Copy an example profile
Copy-Item "examples\web-scraping\ecommerce\amazon-product-details.json" "app\config\profiles\my-scraper.json"

# Run with your custom profile
python main.py --profile my-scraper --url "https://example.com"
```

## Roadmap
- [ ] **Mutli-pdf Scraper**: Support for scraping multiple PDFs in a single run
- [ ] **Mutli-scraper support**: Allow using multiple scraper types in a single profile
- [ ] **Improved Debug Mode**: Enhanced logging and debugging capabilities


## License


## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.