"""
Agent configuration settings for browser-use.
"""
import logging
from ..config_manager import config_manager

logger = logging.getLogger(__name__)

# Agent configuration
USE_VISION = config_manager.get("agent_config.agent.use_vision", False)

SAVE_CONVERSATION_PATH = config_manager.get(
    "agent_config.agent.save_conversation_path", None
)

RUN_MAX_STEPS = int(config_manager.get("agent_config.agent_run.max_steps", 100))

USE_PLANNER_MODEL = config_manager.get(
    "agent_config.agent.use_planner_model", False
)

PLANNER_INTERVAL = int(config_manager.get(
    "agent_config.agent_run.planner_interval", 10
))

# Debug mode
DEBUG_MODE = config_manager.get("browser_config.debug_mode", False)