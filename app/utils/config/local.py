"""
Local configuration settings and profile handling functions.
"""
import os
import sys
import json
import logging
from pathlib import Path
from pydantic import BaseModel, create_model
from ..config_manager import config_manager

logger = logging.getLogger(__name__)

def load_profile_config() -> bool:
    """
    Load a custom configuration file specified as a command-line argument or from local config.

    Returns:
        bool: True if custom config was loaded successfully, False otherwise
    """
    # Check for command-line override first
    if len(sys.argv) > 1 and sys.argv[1].endswith(".yaml"):
        config_override = sys.argv[1]
        config_path = Path(config_override)
        if config_path.exists():
            logger.info(f"Loading config override from command line: {config_override}")
            config_manager.load_specific_config("local", str(config_path))
            return True
        else:
            logger.error(f"Config file not found: {config_override}")
            return False

    # If no command-line override, check for profile reference in local.yaml
    profile_name = config_manager.get("local.profile")
    if profile_name:
        # Build the profile path relative to config directory
        profile_path = (
            Path(config_manager.config_dir) / "profiles" / f"{profile_name}.yaml"
        )
        if profile_path.exists():
            logger.info(f"Loading profile: {profile_name}")
            config_manager.load_specific_config("profile", str(profile_path))
            # set the profile path to environment variable for logging and other uses
            os.environ["PROFILE_PATH"] = str(profile_path)
            return True
        else:
            logger.error(f"Profile not found: {profile_name}")
            logger.error(f"Expected path: {profile_path}")
            return False

    # No override specified, continue with default local config
    return True


def build_content_model() -> BaseModel:
    """
    Parse the content format from the configuration and return the corresponding model.
    """
    # First check for content structure in profile if it exists
    content_structure = config_manager.get("profile.content_structure")

    # Fall back to basic content structure if not found in profile
    if not content_structure:
        return create_model("TextContent", text=(str, ...))

    type_map = {
        "str": (str, ...),
        "int": (int, ...),
        "float": (float, ...),
        "bool": (bool, ...),
    }

    model_name, fields = next(iter(content_structure.items()))
    model_fields = {k: type_map[v] for k, v in fields.items()}

    content_model = create_model(model_name, **model_fields)
    return content_model


def parse_local_config(available_templates: list) -> dict:
    """
    Parse the configuration from profile and/or local configs and set up the environment.

    Args:
        available_templates: List of available task templates

    Returns:
        dict: Dictionary of configuration values
    """
    from ..config.agent import DEBUG_MODE

    # Helper function to get config with profile fallback
    def get_config(key, default=None):
        # Only look in profile configuration, as local should only contain profile reference
        # and optional overrides that should be explicitly checked
        if key == "output_path":
            # Check if output path is set in local config
            value = config_manager.get("local.output_path")
            if value:
                return value

        value = config_manager.get(f"profile.scraper.{key}")

        return value if value is not None else default

    # Get required configuration
    url = get_config("url")
    prompt = get_config("prompt")

    # Validate required configuration
    if not url:
        logger.error("URL is required in profile configuration (profile.scraper.url)")
        return {}

    if not prompt:
        logger.error(
            "Prompt is required in profile configuration (profile.scraper.prompt)"
        )
        return {}

    # Handle additional context
    additional_context = None
    context_config = get_config("context", {})
    if context_config and context_config.get("value"):
        context_format = context_config.get("format")
        context_value = context_config.get("value")

        if context_format == "json":
            try:
                additional_context = json.loads(context_value)
                additional_context = "\n".join(
                    [f"{k}: {v}" for k, v in additional_context.items()]
                )
            except json.JSONDecodeError:
                logger.warning("Failed to parse context as JSON. Using as plain text.")
                additional_context = context_value
        else:
            additional_context = context_value

    # Handle initial actions
    initial_actions = get_config("initial_actions", [])
    if initial_actions:
        parsed_initial_actions = []
        for initial_action in initial_actions:
            action, value = list(initial_action.items())[0]
            if "scroll" in action:
                parsed_initial_actions.append({action: {"amount": value}})
            elif "go_to_url" == action:
                parsed_initial_actions.append({action: {"url": value}})
            else:
                logger.warning(f"Unknown action: {action}. Skipping.")
                continue
        initial_actions = parsed_initial_actions

    # Set the task template
    task_template = get_config("task_template", "default")

    if task_template not in available_templates:
        logger.warning(
            f"Invalid template: {task_template}. Using default template instead."
        )
        task_template = "default"

    # Get output path
    output_path = get_config("output_path")

    # Get profile name for logging
    profile_name = config_manager.get("profile.name")

    # Return all configuration values
    return {
        "url": url,
        "prompt": prompt,
        "additional_context": additional_context,
        "task_template": task_template,
        "initial_actions": initial_actions,
        "profile_name": profile_name,
        "output_path": output_path,
        "debug_mode": DEBUG_MODE,
    }