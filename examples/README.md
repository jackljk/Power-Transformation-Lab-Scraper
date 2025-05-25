# Examples Directory

This directory contains example configurations and use cases for the Power Transformation Lab Scraper. Each subdirectory demonstrates different scraping scenarios and best practices.

## Directory Structure

```
examples/
├── README.md                 # This file
├── USAGE.md                  # Comprehensive usage guide
├── web-scraping/            # Web scraping examples
│   ├── ecommerce/           # E-commerce site examples
│   │   ├── amazon-product-details.json
│   │   └── ebay-auction-monitor.json
│   ├── news-sites/          # News website examples
│   │   ├── bbc-news-extractor.json
│   │   └── reuters-breaking-news.json
│   ├── social-media/        # Social media scraping
│   │   ├── linkedin-company-analyzer.json
│   │   └── twitter-trend-monitor.json
│   └── data-tables/         # Tabular data extraction
│       ├── yahoo-finance-tables.json
│       └── wikipedia-tables.json
├── pdf-extraction/          # PDF processing examples
│   ├── academic-papers/     # Research paper extraction
│   │   └── research-paper-analyzer.json
│   ├── financial-reports/   # Financial document analysis
│   │   └── annual-report-analyzer.json
│   └── technical-docs/      # Technical documentation
│       └── documentation-extractor.json
├── multi-scraper/          # Complex workflows using multiple scrapers
│   ├── company-research-workflow.json
│   └── market-research-pipeline.json
└── advanced-configs/       # Advanced configuration examples
    ├── ecommerce-advanced-monitor.json
    ├── high-volume-news-aggregator.json
    └── secure-document-processing.json
```

## Quick Start Examples

### Basic Web Scraping
See `web-scraping/basic/` for simple website extraction examples.

### PDF Document Processing
See `pdf-extraction/basic/` for PDF document analysis examples.

### Tabular Data Extraction
See `web-scraping/data-tables/` for structured data extraction examples.

## Example Categories

### 1. Web Scraping Examples
- **E-commerce**: Product catalogs, pricing, inventory
- **News Sites**: Articles, headlines, author information
- **Data Tables**: Financial data, statistics, directories
- **Social Media**: Posts, profiles, engagement metrics

### 2. PDF Extraction Examples
- **Academic Papers**: Research data, citations, methodology
- **Financial Reports**: Financial metrics, performance data
- **Technical Documentation**: Specifications, procedures

### 3. Advanced Use Cases
- **Multi-step Workflows**: Complex scraping sequences
- **Custom Templates**: Specialized extraction templates
- **Error Handling**: Robust scraping configurations

## Using Examples

1. **Copy Configuration**: Copy example profile to `app/config/profiles/`
2. **Modify Settings**: Update URLs, file paths, and extraction prompts
3. **Run Example**: Use `python main.py --profile=example_name`
4. **Review Results**: Check output in `results/` directory

## Contributing Examples

To contribute new examples:

1. Create appropriate subdirectory
2. Include complete profile configuration
3. Add sample data or test URLs
4. Document the use case and expected output
5. Test thoroughly before submitting

## Example Testing

All examples should be tested regularly to ensure:
- Configurations are valid
- URLs are accessible
- Expected output format is maintained
- Error handling works correctly

## Getting Help

If you have questions about examples or need help creating configurations for specific use cases, please:

1. Check existing examples for similar patterns
2. Review the main documentation
3. Create an issue with your specific requirements

## Example Profiles Overview

### Web Scraping Examples

#### E-commerce (`web-scraping/ecommerce/`)
- **`amazon-product-details.json`**: Comprehensive Amazon product information extraction including pricing, reviews, specifications, and competitor data. Optimized for dynamic content loading and anti-bot detection avoidance.
- **`ebay-auction-monitor.json`**: Real-time eBay auction monitoring with bidding history, seller information, and time-sensitive data tracking.

#### News Sites (`web-scraping/news-sites/`)
- **`bbc-news-extractor.json`**: Professional news article extraction from BBC News with structured content, metadata, and multimedia handling using Bright Data's reliable proxy network.
- **`reuters-breaking-news.json`**: Breaking news monitoring system with real-time updates, priority classification, and change detection for Reuters news feeds.

#### Social Media (`web-scraping/social-media/`)
- **`linkedin-company-analyzer.json`**: LinkedIn company profile analysis extracting business information, employee insights, and recent activity while respecting platform terms of service.
- **`twitter-trend-monitor.json`**: Twitter/X trend monitoring with sentiment analysis, hashtag tracking, and real-time social media intelligence gathering.

#### Data Tables (`web-scraping/data-tables/`)
- **`yahoo-finance-tables.json`**: Advanced financial data extraction from Yahoo Finance including income statements, balance sheets, and key financial ratios with numerical validation.
- **`wikipedia-tables.json`**: Structured data extraction from Wikipedia articles including statistical tables, infoboxes, and comparative data with proper formatting preservation.

### PDF Extraction Examples

#### Academic Papers (`pdf-extraction/academic-papers/`)
- **`research-paper-analyzer.json`**: Comprehensive research paper analysis extracting abstracts, methodology, results, citations, and mathematical content with academic structure recognition.

#### Financial Reports (`pdf-extraction/financial-reports/`)
- **`annual-report-analyzer.json`**: Professional financial report processing for annual reports and 10-K filings with quantitative data extraction and risk factor analysis.

#### Technical Documentation (`pdf-extraction/technical-docs/`)
- **`documentation-extractor.json`**: Technical manual and API documentation processing with code example extraction, installation instructions, and troubleshooting information.

### Multi-Scraper Workflows

#### Complex Research (`multi-scraper/`)
- **`company-research-workflow.json`**: End-to-end company research pipeline combining website analysis, financial data extraction, document processing, and sentiment analysis for comprehensive business intelligence.
- **`market-research-pipeline.json`**: Market research automation combining competitor analysis, industry reports, and pricing data for strategic decision-making.

### Advanced Configurations

#### Production-Ready (`advanced-configs/`)
- **`ecommerce-advanced-monitor.json`**: Enterprise-grade e-commerce monitoring with anti-detection measures, session management, proxy rotation, and automated alerts.
- **`high-volume-news-aggregator.json`**: High-performance news aggregation system with load balancing, distributed processing, and quality assurance for large-scale operations.
- **`secure-document-processing.json`**: Security-focused PDF processing with encryption handling, PII detection, data privacy controls, and compliance features for sensitive documents.
