# Custom Task Templates

This guide explains how to create and customize task templates for the Power Transformation Lab Scraper.

## Overview

Task templates define how the AI approaches different types of extraction tasks. They provide pre-configured prompts and instructions optimized for specific scenarios like tabular data extraction, document analysis, or general web scraping.

## Understanding Task Templates

### Template Structure

Task templates are defined in `app/templates/task_templates.py` with the following structure:

```python
TASK_TEMPLATES = {
    "template_name": {
        "task_format": """
            Template prompt with {placeholders}
            
            Requirements:
            1. Specific instructions
            2. Format requirements
        """
    }
}
```

### Available Placeholders

Templates support dynamic placeholders that are replaced at runtime:

- `{prompt}`: User-provided extraction prompt
- `{url}`: Target URL (for web scrapers)
- `{website}`: Website name extracted from URL
- `{data_category}`: Category of data being extracted
- `{data_points}`: Specific data points to extract
- `{no_pages}`: Instructions for single vs multi-page extraction
- `{filters}`: Any filtering criteria

Which are used for different scraping scenarios more customization.dynamic placeholder is a **WIP** 

**See Templates to get a better understanding**

## Built-in Templates

### 1. Default Template
```python
"default": {
    "task_format": """
        From the provided webpage, extract information about: "{prompt}"
        
        Requirements:
        1. The extracted information must be 100% factual and found on the page (DO NOT Infer Data).
        2. Only include information that is relevant to the prompt.
    """
}
```

**Use Case**: General-purpose information extraction  
**Best For**: Most web scraping tasks requiring factual data extraction

### 2. Tabular Extraction Template
```python
"tabular_extraction": {
    "task_format": """
    Extract structured data from {website} about {data_category}.

    1. Navigate to {url}
    2. Identify the table or structured data containing information about {data_points}
    3. Extract all rows and columns while preserving the relationship between data points
    {no_pages}
    {filters}

    Format the extracted data in JSON format with appropriate headers following AgentOutput Format. 
    If any data points are missing, mark them as a null value rather than leaving them blank.
    """
}
```

**Use Case**: Extracting data from tables, lists, or structured layouts  
**Best For**: Structured data in tabular format already

### 3. PDF Default Template
```python
"pdf_default": {
    "task_format": """
    From the provided PDF, extract information about: "{prompt}"

    Requirements:
    1. The extracted information must be 100% factual and found on the page (DO NOT Infer Data).
    2. Only include information that is relevant to the prompt.
    """
}
```

**Use Case**: PDF document processing  
**Best For**: Academic papers, reports, documentation -- PDFS

## Creating Custom Templates

### Step 1: Design Your Template

1. **Identify the Use Case**: What specific type of extraction does this template optimize for?
2. **Define Requirements**: What specific instructions should the AI follow?
3. **Consider Output Format**: How should the extracted data be structured?

### Step 2: Write the Template

Create a new template entry in `app/templates/task_templates.py`:

```python
"my_custom_template": {
    "task_format": """
        Your custom template instructions here.
        
        Use {prompt} to include the user's extraction request.
        
        Specific requirements:
        1. Instruction 1
        2. Instruction 2
        3. Output format requirements
    """
}
```

### Step 3: Test Your Template

Create a test profile using your new template:

```yaml
name: "test_custom_template"

scraper:
  scraper_type: "browser_use"
  url: "https://example.com"
  
  prompt:
    task_template: "my_custom_template"
    text: "Extract the information I need"

content_structure:
  # Define expected output structure
```


## Tailoring Templates for Specific Use Cases

Keep in mind that the default templates work most of the time, but crafting templates for your specific needs can significantly improve extraction accuracy. Custom templates allow you to:

1. **Optimize for domain-specific data** - Financial, medical, or technical content often benefits from specialized instructions
2. **Handle unusual data formats** - When dealing with non-standard layouts or mixed content types
3. **Increase extraction precision** - By providing explicit guidance on what data to prioritize
4. **Improve consistency** - By standardizing how edge cases and ambiguities are handled

Consider creating custom templates when dealing with:
- Complex nested data structures
- Industry-specific terminology
- Multiple data formats on a single page
- Strict compliance or accuracy requirements

The time invested in template customization typically pays off through higher quality data and fewer extraction errors.

### News Article Extraction Template Example
```python
"news_extraction": {
    "task_format": """
        Extract news article information from: "{prompt}"
        
        Required Fields:
        1. Headline/Title (exact text from the page)
        2. Publication date and time
        3. Author name(s)
        4. Article body/content (main text only, exclude ads/navigation)
        5. Category/Section if available
        6. Tags or keywords if present
        
        Quality Requirements:
        - Only extract factual information visible on the page
        - Preserve original formatting for quotes and important text
        - Do not include advertisements, related articles, or navigation elements
        - If publication date is not explicitly stated, mark as null
        
        Output Format:
        Structure the data according to the provided schema with proper field names.
    """
}
```

### E-commerce Product Template Example
```python
"ecommerce_extraction": {
    "task_format": """
        Extract product information about: "{prompt}"
        
        Product Data to Extract:
        1. Product name/title (exact as displayed)
        2. Current price (numerical value and currency)
        3. Original price if on sale
        4. Availability status (in stock, out of stock, limited quantity)
        5. Product rating (numerical score)
        6. Number of reviews/ratings
        7. Product description (main description only)
        8. Key features or specifications
        9. Product images URLs
        10. Seller/brand information
        
        Price Handling:
        - Extract numerical values only for prices
        - Note currency if displayed
        - If multiple prices shown, prioritize current/sale price
        
        Accuracy Requirements:
        - Only extract information explicitly shown on the product page
        - Do not infer or calculate missing information
        - Mark unavailable fields as null rather than guessing
    """
}
```

### Academic Research Template Example
```python
"academic_research": {
    "task_format": """
        Extract academic research information about: "{prompt}"
        
        Research Paper Elements:
        1. Title (complete and exact)
        2. Authors (all authors with affiliations if available)
        3. Abstract (complete text)
        4. Keywords or subject terms
        5. Publication venue (journal, conference, etc.)
        6. Publication date/year
        7. DOI or other identifiers
        8. Research methodology (if clearly described)
        9. Key findings or results (main conclusions only)
        10. References count (if displayed)
        
        Content Guidelines:
        - Extract only factual information from the document
        - Preserve scientific terminology and notation
        - Do not summarize or interpret findings
        - Include exact quotes for key conclusions
        - Note if information is not available rather than inferring
        
        Special Handling:
        - For mathematical expressions, preserve original notation
        - For tables/figures, describe what data they contain
        - Extract methodology section details if specifically requested
    """
}
```

### Financial Data Template Example
```python
"financial_extraction": {
    "task_format": """
        Extract financial information about: "{prompt}"
        
        Financial Metrics to Extract:
        1. Company name and ticker symbol
        2. Current stock price and currency
        3. Price change (absolute and percentage)
        4. Trading volume
        5. Market capitalization
        6. Financial ratios (P/E, P/B, etc.)
        7. Revenue figures (latest period)
        8. Profit/loss information
        9. Dividend information if available
        10. Date/time of data
        
        Data Quality Requirements:
        - Extract exact numerical values as displayed
        - Preserve units and time periods for all metrics
        - Note the date/time when data was retrieved
        - Do not calculate or derive ratios not explicitly shown
        - Mark missing data as null, not zero
        
        Format Specifications:
        - Use consistent number formatting
        - Preserve currency symbols and units
        - Include data source timestamps
        - Structure data according to provided schema
    """
}
```

### Multi-Language Support Template Example
```python
"multilingual_template": {
    "task_format": """
        Extract information in the source language: "{prompt}"
        
        Language Handling:
        - Preserve original language for extracted text
        - Translate field names to English for consistency
        - Note the detected language in metadata
        
        Requirements:
        - Do not translate content unless specifically requested
        - Maintain cultural context and meaning
    """
}
```

## Template Best Practices

### 1. Clear Instructions
- Use specific, actionable language
- Avoid ambiguous terms
- Provide examples when helpful

### 2. Quality Requirements
- Emphasize factual accuracy
- Specify what NOT to do (don't infer, don't calculate)
- Include error handling instructions

### 3. Output Formatting
- Specify exact output structure requirements
- Handle missing data consistently
- Preserve important formatting

For output see 

### 4. Use Case Optimization
- Tailor instructions to specific data types
- Include domain-specific guidance
- Address common extraction challenges



## Troubleshooting Templates

### Common Issues

1. **Inconsistent Results**: Template instructions may be too vague
2. **Missing Data**: Template may not account for data variations
3. **Incorrect Format**: Output format instructions may be unclear
4. **Poor Performance**: Template may be too complex or inefficient

### Debugging Steps

1. Enable debug mode for detailed logs
2. Test with simple, known data sources
3. Compare results with expected output
4. Iterate on template instructions
5. Validate with multiple test cases



This comprehensive guide should help you create effective custom templates for your specific extraction needs. Remember to test thoroughly and iterate based on real-world results.

Also always remember that AI can be incorrect and be sure to perform some simple validation to ensure high data quality.
