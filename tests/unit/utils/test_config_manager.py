import os
import pytest
import tempfile
from pathlib import Path
import yaml

from app.utils.config_manager import ConfigManager

@pytest.fixture
def temp_config_dir():
    """Create a temporary directory with test config files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test config file
        test_config = {
            "test_section": {
                "key1": "value1",
                "key2": 123,
                "nested": {
                    "nested_key": "nested_value"
                }
            }
        }
        
        config_path = Path(temp_dir) / "test_config.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(test_config, f)
            
        # Create a test secrets file
        test_secrets = {
            "secrets": {
                "api_key": "test_api_key"
            }
        }
        
        secrets_path = Path(temp_dir) / "secrets.yaml"
        with open(secrets_path, 'w') as f:
            yaml.dump(test_secrets, f)
            
        yield temp_dir

def test_config_manager_init(temp_config_dir):
    """Test ConfigManager initialization with custom config directory."""
    config_manager = ConfigManager(config_dir=temp_config_dir)
    assert "test_config" in config_manager.configs
    assert config_manager.configs["test_config"]["test_section"]["key1"] == "value1"

def test_config_manager_get(temp_config_dir):
    """Test the get method for retrieving configuration values."""
    config_manager = ConfigManager(config_dir=temp_config_dir)
    
    # Test getting a simple value
    assert config_manager.get("test_config.test_section.key1") == "value1"
    
    # Test getting a nested value
    assert config_manager.get("test_config.test_section.nested.nested_key") == "nested_value"
    
    # Test getting a value with default
    assert config_manager.get("non_existent.path", "default") == "default"

def test_config_manager_get_secret(temp_config_dir):
    """Test retrieving secrets with environment variable fallback."""
    config_manager = ConfigManager(config_dir=temp_config_dir)
    
    # Test getting a secret from the file
    assert config_manager.get_secret("secrets.api_key") == "test_api_key"
    
    # Test environment variable override
    os.environ["TEST_API_KEY"] = "env_api_key"
    assert config_manager.get_secret("secrets.api_key", "TEST_API_KEY") == "env_api_key"
    
    # Clean up environment
    del os.environ["TEST_API_KEY"]

def test_config_manager_reload(temp_config_dir):
    """Test reloading configuration files."""
    config_manager = ConfigManager(config_dir=temp_config_dir)
    
    # Modify the config file
    test_config = {
        "test_section": {
            "key1": "updated_value",
        }
    }
    
    config_path = Path(temp_config_dir) / "test_config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(test_config, f)
    
    # Reload and verify the updated value
    config_manager.reload()
    assert config_manager.get("test_config.test_section.key1") == "updated_value"