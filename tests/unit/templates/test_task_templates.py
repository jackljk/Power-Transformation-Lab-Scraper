import pytest
from app.templates.task_templates import get_task_template, get_available_templates, TASK_TEMPLATES

def test_get_available_templates():
    """Test that get_available_templates returns the correct list of templates."""
    templates = get_available_templates()
    assert isinstance(templates, list)
    assert len(templates) > 0
    assert "default" in templates
    assert set(templates) == set(TASK_TEMPLATES.keys())

def test_get_task_template_valid():
    """Test retrieving a valid template."""
    default_template = get_task_template("default")
    assert "task_format" in default_template
    assert isinstance(default_template["task_format"], str)
    
    # Test another template if available
    if "summary" in TASK_TEMPLATES:
        summary_template = get_task_template("summary")
        assert "task_format" in summary_template
        assert "output_format" in summary_template

def test_get_task_template_invalid():
    """Test that requesting an invalid template returns the default template."""
    invalid_template = get_task_template("non_existent_template")
    assert invalid_template == TASK_TEMPLATES["default"]

def test_template_content_structure():
    """Test that all templates have the required structure."""
    for template_name, template in TASK_TEMPLATES.items():
        assert "task_format" in template
        assert isinstance(template["task_format"], str)
        
        # All templates except default should have output_format
        if template_name != "default":
            assert "output_format" in template
            assert isinstance(template["output_format"], str)