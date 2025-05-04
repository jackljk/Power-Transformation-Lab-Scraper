import pytest
from pydantic import ValidationError
from app.models.text_models import Citation, ScrapedResult
from app.models.output_format_models import Citation as OutputCitation

def test_citation_model():
    """Test the Citation model validation."""
    # Valid citation
    citation = Citation(
        text="Test citation text",
        source_url="https://example.com",
        selector_path="div > p.content",
        confidence_score=0.95
    )
    
    assert citation.text == "Test citation text"
    assert citation.source_url == "https://example.com"
    assert citation.selector_path == "div > p.content"
    assert citation.confidence_score == 0.95
    
    # Test with missing required fields
    with pytest.raises(ValidationError):
        Citation(
            text="Test citation text",
            selector_path="div > p.content",
            confidence_score=0.95
        )
    
    # Test with invalid confidence score format
    with pytest.raises(ValidationError):
        Citation(
            text="Test citation text",
            source_url="https://example.com",
            selector_path="div > p.content",
            confidence_score="high"  # Should be a float
        )

def test_output_citation_model():
    """Test the OutputCitation model validation."""
    # Valid citation
    citation = OutputCitation(
        source_text="Example text from webpage",
        location="Header section",
        location_url="https://example.com#:~:text=Example%20text%20from%20webpage"
    )
    
    assert citation.source_text == "Example text from webpage"
    assert citation.location == "Header section"
    assert citation.location_url == "https://example.com#:~:text=Example%20text%20from%20webpage"
    
    # Test with missing required fields
    with pytest.raises(ValidationError):
        OutputCitation(
            source_text="Example text from webpage",
            location="Header section"
            # Missing location_url
        )

def test_scraped_result_model():
    """Test the ScrapedResult model validation."""
    # Valid scraped result
    result = ScrapedResult(
        content="Extracted content",
        citations=[
            Citation(
                text="Test citation text",
                source_url="https://example.com",
                selector_path="div > p.content",
                confidence_score=0.95
            )
        ],
        format_type="text",
        prompt="Extract information about X",
        url="https://example.com"
    )
    
    assert result.content == "Extracted content"
    assert len(result.citations) == 1
    assert result.format_type == "text"
    assert result.prompt == "Extract information about X"
    assert result.url == "https://example.com"
    
    # Test with empty citations list
    result = ScrapedResult(
        content="Extracted content",
        citations=[],
        format_type="text",
        prompt="Extract information about X",
        url="https://example.com"
    )
    
    assert len(result.citations) == 0