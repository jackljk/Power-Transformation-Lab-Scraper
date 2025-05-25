# Using Example Profiles

This guide explains how to use the example profiles provided in this directory and how to customize them for your specific needs.

## Quick Start

### Using an Example Profile

1. **Copy an example profile** to your profiles directory:
```powershell
Copy-Item "examples\web-scraping\ecommerce\amazon-product-details.json" "app\config\profiles\my-amazon-scraper.json"
```

2. **Customize the profile** for your specific needs:
   - Update `target_url` with your specific URL pattern
   - Modify `output_format` to match your data requirements
   - Adjust `scraper_kwargs` for your use case

3. **Run the scraper** with your custom profile:
```powershell
python main.py --profile my-amazon-scraper --url "https://www.amazon.com/dp/B08N5WRWNW"
```

## Example Categories

### Web Scraping Examples

#### E-commerce (`examples/web-scraping/ecommerce/`)
- **`amazon-product-details.json`**: Extract comprehensive product information from Amazon
- **`ebay-auction-monitor.json`**: Monitor eBay auctions for bidding and seller information

**Use Cases:**
- Price monitoring and comparison
- Product catalog building
- Inventory tracking
- Competitor analysis

#### News Sites (`examples/web-scraping/news-sites/`)
- **`bbc-news-extractor.json`**: Extract full news articles from BBC News
- **`reuters-breaking-news.json`**: Monitor Reuters for breaking news updates

**Use Cases:**
- News aggregation
- Media monitoring
- Content research
- Sentiment analysis

#### Data Tables (`examples/web-scraping/data-tables/`)
- **`yahoo-finance-tables.json`**: Extract financial data tables from Yahoo Finance
- **`wikipedia-tables.json`**: Extract structured data tables from Wikipedia

**Use Cases:**
- Financial data collection
- Research data gathering
- Statistical analysis
- Market research

### PDF Extraction Examples

#### Academic Papers (`examples/pdf-extraction/academic-papers/`)
- **`research-paper-analyzer.json`**: Extract structured information from research papers

**Use Cases:**
- Literature reviews
- Research analysis
- Citation extraction
- Academic research

#### Financial Reports (`examples/pdf-extraction/financial-reports/`)
- **`annual-report-analyzer.json`**: Extract financial information from annual reports

**Use Cases:**
- Investment research
- Financial analysis
- Compliance monitoring
- Risk assessment

#### Technical Documentation (`examples/pdf-extraction/technical-docs/`)
- **`documentation-extractor.json`**: Extract information from technical manuals and API docs

**Use Cases:**
- Documentation analysis
- API reference extraction
- Technical research
- Knowledge base building

### Multi-Scraper Workflows

#### Complex Research (`examples/multi-scraper/`)
- **`company-research-workflow.json`**: Comprehensive company research combining multiple sources
- **`market-research-pipeline.json`**: End-to-end market research workflow

**Use Cases:**
- Investment research
- Due diligence
- Market analysis
- Competitive intelligence

### Advanced Configurations

#### High-Performance (`examples/advanced-configs/`)
- **`ecommerce-advanced-monitor.json`**: Advanced e-commerce monitoring with anti-detection
- **`high-volume-news-aggregator.json`**: High-performance news aggregation
- **`secure-document-processing.json`**: Secure PDF processing with privacy controls

**Use Cases:**
- Large-scale data collection
- Production environments
- Sensitive data handling
- High-availability systems

## Customization Guide

### Basic Customization

1. **URL Patterns**: Replace placeholder URLs with your target sites
```json
{
    "target_url": "https://yoursite.com/page/{parameter}"
}
```

2. **Output Format**: Modify the output structure to match your needs
```json
{
    "output_format": {
        "your_field": "Description of what to extract",
        "nested_data": {
            "sub_field": "Nested information"
        }
    }
}
```

3. **Task Prompt**: Customize the extraction instructions
```json
{
    "task_prompt": "Extract specific information you need including details about format, structure, and any special requirements"
}
```

### Advanced Customization

#### Browser Configuration
```json
{
    "scraper_kwargs": {
        "browser_type": "chromium|firefox|webkit",
        "headless": true,
        "viewport": {"width": 1920, "height": 1080},
        "timeout": 30000,
        "extra_actions": ["custom_action_1", "custom_action_2"]
    }
}
```

#### Proxy Configuration
```json
{
    "scraper_kwargs": {
        "proxy_config": {
            "type": "residential|datacenter",
            "rotation": "per_request|session",
            "country": "US|UK|EU"
        }
    }
}
```

#### Error Handling
```json
{
    "retry_config": {
        "max_retries": 3,
        "retry_delay": 5,
        "backoff_multiplier": 2
    }
}
```

## Profile Validation

Before using a customized profile, validate it using the built-in validation:

```powershell
python main.py --validate-profile my-custom-profile.json
```

## Performance Tips

### For Web Scraping
- Use `bright_data` scraper for better performance on simple pages
- Use `browser_use` scraper for JavaScript-heavy sites
- Configure appropriate timeouts and retries
- Use headless mode for better performance

### For PDF Processing
- Optimize chunk sizes for your document types
- Use batch processing for multiple documents
- Configure appropriate model parameters for your content

### For Multi-Scraper Workflows
- Plan execution order for data dependencies
- Use parallel execution where possible
- Implement proper error handling and fallbacks
- Save intermediate results for debugging

## Common Issues and Solutions

### Authentication
For sites requiring login, add authentication configuration:
```json
{
    "authentication": {
        "type": "login_form|api_key|oauth",
        "credentials": {
            "username": "your_username",
            "password": "your_password"
        }
    }
}
```

### Rate Limiting
Handle rate limits with proper delays:
```json
{
    "rate_limiting": {
        "requests_per_minute": 60,
        "delay_between_requests": 1,
        "respect_robots_txt": true
    }
}
```

### Data Quality
Improve extraction quality:
```json
{
    "quality_control": {
        "min_content_length": 100,
        "required_fields": ["title", "content"],
        "validation_rules": ["no_empty_values", "valid_urls"]
    }
}
```

## Testing Your Profiles

1. **Start with a small test**:
```powershell
python main.py --profile your-profile --url "single-test-url" --debug
```

2. **Check the results** in the `results/` directory

3. **Review logs** for any issues or improvements

4. **Iterate and refine** your profile configuration

## Next Steps

- Explore the [Profile Configuration Guide](../docs/profile-configuration.md) for detailed parameter documentation
- Read the [Custom Templates Guide](../docs/custom-templates.md) for creating custom task templates
- Check the [Troubleshooting Guide](../docs/troubleshooting.md) for common issues and solutions
