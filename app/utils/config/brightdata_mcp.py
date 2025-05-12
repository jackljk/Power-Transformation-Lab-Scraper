from mcp import StdioServerParameters
from ..config_manager import config_manager
import logging

logger = logging.getLogger(__name__)

"""
    MCP configuration for Bright Data
"""

WEB_UNLOCKER_ZONE = config_manager.get("mcp_config.brightdata_mcp.web_unlocker_zone", None)
BROWSER_AUTH = config_manager.get("mcp_config.brightdata_mcp.browser_auth", None)
BRIGHTDATA_API_KEY = config_manager.get_secret("secrets.mcp.brightdata_api_key", None)


def define_mcp_server_params() -> StdioServerParameters:
    """
    Define the server parameters for the MCP server.
    """
    assert WEB_UNLOCKER_ZONE, "WEB_UNLOCKER_ZONE is not set in the configuration"
    assert BROWSER_AUTH, "BROWSER_AUTH is not set in the configuration"
    assert BRIGHTDATA_API_KEY, "BRIGHTDATA_API_KEY is not set in the configuration"
    logger.debug("MCP server parameters are set correctly.")

    return StdioServerParameters(
        command="npx",
        env={
            "API_TOKEN": BRIGHTDATA_API_KEY,
            "BROWSER_AUTH": BROWSER_AUTH,
            "WEB_UNLOCKER_ZONE": WEB_UNLOCKER_ZONE,
        },
        args=["@brightdata/mcp"],
    )