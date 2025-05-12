import yaml
import os
from pathlib import Path
from typing import Any, Dict
import logging 

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    A class to manage YAML configuration files with support for reloading
    and hierarchical access.
    """

    def __init__(self, config_dir: str = None):
        """
        Initialize the ConfigManager.
        
        Args:
            config_dir: Directory containing configuration files (default: app/config)
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Default to app/config relative to the current file
            self.config_dir = Path(__file__).parent.parent / "config"
        
        self.configs = {}
        self._load_configs()
    
    def _load_configs(self) -> None:
        """Load all YAML files from the config directory."""
        if not self.config_dir.exists():
            logger.warning(f"Warning: Config directory not found at {self.config_dir}")
            return
        
        for config_file in self.config_dir.glob("*.yaml"):
            config_name = config_file.stem
            try:
                with open(config_file, 'r') as f:
                    self.configs[config_name] = yaml.safe_load(f)
                logger.info(f"Loaded configuration from {config_file}")
            except Exception as e:
                logger.error(f"Error loading {config_file}: {str(e)}")
                self.configs[config_name] = {}
    
    def reload(self) -> None:
        """Reload all configuration files."""
        self.configs = {}
        self._load_configs()
        
    def load_specific_config(self, config_name: str, file_path: str) -> None:
        """
        Load a specific configuration file and assign it to a config key.
        
        Args:
            config_name: The name to use for the configuration in the configs dictionary
            file_path: Path to the configuration file to load
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"Warning: Config file not found at {file_path}")
                return
                
            with open(file_path, 'r', encoding='utf-8') as f:
                self.configs[config_name] = yaml.safe_load(f)
            logger.info(f"Loaded specific configuration from {file_path} as {config_name}")
        except Exception as e:
            logger.error(f"Error loading specific config {file_path}: {str(e)}")
            self.configs[config_name] = {}
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation path.
        
        Args:
            path: Dot-notation path to the config value (e.g., "browser_config.browser.wait_times.timeout")
            default: Default value if the path doesn't exist
            
        Returns:
            The configuration value or the default if not found
        """
        parts = path.split('.')
        # First part should be the config file name
        if parts[0] not in self.configs:
            return default
        
        current = self.configs[parts[0]]
        
        # Navigate through the nested structure
        for part in parts[1:]:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    
    def get_all(self, config_name: str) -> Dict:
        """
        Get an entire configuration section.
        
        Args:
            config_name: Name of the configuration file (without extension)
            
        Returns:
            The entire configuration dictionary or empty dict if not found
        """
        return self.configs.get(config_name, {})

    def get_secret(self, path: str, env_var: str = None) -> Any:
        """
        Get a secret from the secrets file or environment variable.
        Environment variables take precedence over secrets file.
        
        Args:
            path: Dot-notation path to the secret in secrets.yaml
            env_var: Environment variable name that would override this setting
            
        Returns:
            The secret value or None if not found
        """
        # Check environment variable first (highest priority)
        if env_var and env_var in os.environ:
            return os.environ[env_var]
        # Try the secrets file next
        return self.get(path, None)


# Create a singleton instance
config_manager = ConfigManager()