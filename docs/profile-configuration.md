# Profile Configuration Reference

This document provides detailed information about all available configuration options for scraper profiles.

## Profile Structure Overview

```yaml
# Profile metadata
name: "profile_name"

# Scraper configuration
scraper:
  scraper_type: "browser_use"  # Required
  url: "https://example.com"   # Required for web scrapers
  filepath: "path/to/file.pdf" # Required for PDF scraper
  
  prompt:
    task_template: "default"   # Required
    text: "extraction prompt"  # Required
  
  additional_context:          # Optional
    format: "text"
    value: "context information"
  
  initial_actions:             # Optional (browser_use only)
    - action_type: parameters

# Output structure definition
content_structure:             # Optional but recommended
  DataType:
    field_name: data_type
```

## Configuration Parameters

### Core Parameters

#### `name` (string, required)
- **Description**: Identifier for the profile used in logs and results
- **Format**: Lowercase letters, numbers, underscores, and hyphens only
- **Example**: `"wikipedia_extraction"`

#### `scraper.scraper_type` (string, required)
- **Description**: Specifies which scraping technology to use
- **Options**:
  - `"browser_use"`: Browser automation with AI
  - `"bright_data_mcp"`: Proxy-based scraping
  - `"pdf_scraper"`: PDF document processing
- **Example**: `"browser_use"`

### Source Configuration

#### `scraper.url` (string, required for web scrapers)
- **Description**: Target URL for web scraping
- **Format**: Valid HTTP/HTTPS URL
- **Example**: `"https://en.wikipedia.org/wiki/Python"`

#### `scraper.filepath` (string or array, required for PDF scraper)
- **Description**: Path(s) to PDF file(s) for processing
- **Formats**:
  - Single file: `"data/document.pdf"`
  - Multiple files: `["data/doc1.pdf", "data/doc2.pdf"]`
- **Notes**: Paths are relative to project root

### Prompt Configuration

#### `scraper.prompt.task_template` (string, required)
- **Description**: Template type for extraction task
- **Options**:
  - `"default"`: General-purpose extraction
  - `"tabular_extraction"`: Structured data extraction
  - `"pdf_default"`: PDF-optimized extraction
- **Example**: `"default"`

#### `scraper.prompt.text` (string, required)
- **Description**: Natural language description of what to extract
- **Format**: Clear, specific instructions
- **Example**: `"Extract product names, prices, and availability status"`

### Additional Context (Optional)

#### `scraper.additional_context.format` (string)
- **Description**: Format of additional context data
- **Options**:
  - `"text"`: Plain text context
  - `"json"`: Structured JSON context
- **Example**: `"text"`

#### `scraper.additional_context.value` (string)
- **Description**: Additional information to guide extraction
- **Format**: Depends on `format` parameter
- **Examples**:
  - Text: `"Focus on current prices only"`
  - JSON: `'{"currency": "USD", "date_range": "2025"}'`

### Initial Actions (Browser-Use Only)

#### `scraper.initial_actions` (array, optional)
- **Description**: Actions to perform before extraction
- **Format**: Array of action objects
- **Available Actions**:

##### Scroll Actions
```yaml
- scroll_down: 500    # Scroll down 500 pixels
- scroll_up: 300      # Scroll up 300 pixels
```

##### Navigation Actions
```yaml
- go_to_url: "https://example.com/page"  # Navigate to URL
```

##### Wait Actions
```yaml
- wait: 2000          # Wait 2 seconds
```

##### Click Actions
```yaml
- click_by_xpath: "//button[@id='submit']"  # Click element by XPath
```

### Content Structure (Optional but Recommended)

#### `content_structure` (object)
- **Description**: Defines the expected structure of extracted data
- **Format**: Nested object with data types
- **Benefits**: Ensures consistent output format, improves extraction accuracy

#### Data Types
- `str`: String/text data
- `int`: Integer numbers
- `float`: Decimal numbers
- `bool`: Boolean (true/false)
- `list`: Array of values
- `dict`: Nested object

#### Example Structures

##### Simple Product Data
```yaml
content_structure:
  Products:
    name: str
    price: float
    in_stock: bool
    description: str
```

##### Complex Nested Data
```yaml
content_structure:
  Articles:
    title: str
    author: str
    publication_date: str
    content: str
    tags: list
    metadata:
      word_count: int
      reading_time: int
      category: str
```

##### Tabular Data
```yaml
content_structure:
  Companies:
    company_name: str
    revenue: float
    employees: int
    founded_year: int
    industry: str
    headquarters: str
```

## Scraper-Specific Configurations

### Browser-Use Scraper

#### Optimal Use Cases
- Interactive websites requiring clicks/scrolls
- JavaScript-heavy applications
- Sites with dynamic content loading
- Complex navigation flows

#### Configuration Tips
```yaml
scraper:
  scraper_type: "browser_use"
  url: "https://example.com"
  
  initial_actions:
    - scroll_down: 400          # Load dynamic content
    - wait: 3000                # Wait for content to load
    - click_by_xpath: "//button[@class='load-more']"
    - wait: 2000
    - scroll_down: 400
```

### Bright Data MCP Scraper

#### Optimal Use Cases
- Large-scale data collection
- Sites with anti-bot protection
- Fast, efficient scraping
- Public data repositories

#### Configuration Tips
```yaml
scraper:
  scraper_type: "bright_data_mcp"
  url: "https://example.com"
  
  additional_context:
    format: "text"
    value: "Use residential proxies for this request"
```

### PDF Scraper

#### Optimal Use Cases
- Academic papers and research documents
- Financial reports and statements
- Technical documentation
- Multi-page document analysis

#### Configuration Tips
```yaml
scraper:
  scraper_type: "pdf_scraper"
  filepath: ["data/report1.pdf", "data/report2.pdf"]
  
  prompt:
    task_template: "pdf_default"
    text: "Extract financial metrics from quarterly reports"
  
  additional_context:
    format: "text"
    value: "Focus on tables containing numerical data. The PDFs are quarterly financial reports."
```

## Profile Examples by Use Case

### E-commerce Product Extraction
```yaml
name: "ecommerce_products"

scraper:
  scraper_type: "browser_use"
  url: "https://shop.example.com/products"
  
  prompt:
    task_template: "default"
    text: "Extract product information including names, prices, ratings, and availability"
  
  initial_actions:
    - scroll_down: 500
    - wait: 2000
    - scroll_down: 500

content_structure:
  Products:
    name: str
    price: float
    rating: float
    reviews_count: int
    availability: str
    image_url: str
```

### Academic Paper Analysis
```yaml
name: "research_paper_analysis"

scraper:
  scraper_type: "pdf_scraper"
  filepath: "data/research_papers/"
  
  prompt:
    task_template: "pdf_default"
    text: "Extract methodology, key findings, and conclusions from research papers"
  
  additional_context:
    format: "text"
    value: "Focus on the abstract, methodology section, results, and conclusion sections"

content_structure:
  Papers:
    title: str
    authors: list
    abstract: str
    methodology: str
    key_findings: list
    conclusions: str
    publication_year: int
```

### News Article Collection
```yaml
name: "news_collection"

scraper:
  scraper_type: "bright_data_mcp"
  url: "https://news.example.com"
  
  prompt:
    task_template: "default"
    text: "Extract article headlines, summaries, publication dates, and authors"

content_structure:
  Articles:
    headline: str
    summary: str
    author: str
    publication_date: str
    category: str
    url: str
```

## Validation and Testing

### Profile Validation
Before running, validate your profile:
1. Check YAML syntax
2. Verify required fields are present
3. Ensure file paths exist (for PDF scraper)
4. Test URLs are accessible (for web scrapers)

### Testing Strategies
1. **Start Simple**: Begin with basic extraction, then add complexity
2. **Use Debug Mode**: Enable debug logging for detailed execution traces
3. **Iterative Refinement**: Adjust prompts based on initial results
4. **Content Structure Validation**: Ensure output matches expected format

### Common Issues and Solutions

#### Issue: Inconsistent Output Format
**Solution**: Define detailed `content_structure` with specific field types

#### Issue: Missing Data in Results
**Solution**: 
- Refine the extraction prompt
- Add relevant context information
- Adjust initial actions for dynamic content

#### Issue: PDF Extraction Errors
**Solution**:
- Verify PDF is text-based (not scanned image)
- Check file permissions and paths
- Use more specific prompts for complex documents

## Best Practices

1. **Clear Prompts**: Write specific, actionable extraction prompts
2. **Structured Output**: Always define `content_structure` for consistent results
3. **Context Information**: Provide relevant context to improve extraction accuracy
4. **Progressive Actions**: For browser automation, build up actions step by step
5. **Error Handling**: Include fallback strategies in your workflow
6. **Documentation**: Comment complex configurations for future reference

## Advanced Configuration

### Dynamic Content Handling
```yaml
initial_actions:
  - scroll_down: 500
  - wait: 3000              # Wait for AJAX content
  - click_by_xpath: "//button[contains(@class, 'load-more')]"
  - wait: 2000
  - scroll_down: 500
```

### Multi-page Navigation
```yaml
initial_actions:
  - scroll_down: 800
  - go_to_url: "https://example.com/page2"
  - scroll_down: 800
  - go_to_url: "https://example.com/page3"
```

### Complex Data Structures
```yaml
content_structure:
  Companies:
    basic_info:
      name: str
      ticker: str
      market_cap: float
    financial_data:
      revenue: float
      profit_margin: float
      debt_ratio: float
    metrics:
      pe_ratio: float
      dividend_yield: float
      beta: float
```
