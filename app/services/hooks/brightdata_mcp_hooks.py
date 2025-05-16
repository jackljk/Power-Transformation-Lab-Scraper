import json
import os

import logging

logger = logging.getLogger(__name__)


def log_response(reponse):
    """
    Log the response from the MCP.
    """
    # Setup the results path for logging
    results_env = os.getenv("RESULTS_PATH")
    if not results_env:
        logging.error(
            "RESULTS_PATH environment variable is not set. Skipping page content saving."
        )
        return
    logs = os.path.join(results_env, "mcp_logs")
    os.makedirs(logs, exist_ok=True)
    
    messages = reponse.get("messages", [])
    mcp_log = {
        'print_version': [],
        'json_view': {},
    }
    for message in messages:
        mcp_log['print_version'].append(message.pretty_repr())
        mcp_log['json_view']['tool_calls'] = message.tool_calls
        mcp_log['json_view']['content'] = message.content
        
    # Save the log to a file
    print_version_path = os.path.join(
        logs, "print_version.json"
    )
    json_view_path = os.path.join(
        logs, "json_view.json"
    )
    os.makedirs(os.path.dirname(print_version_path), exist_ok=True)
    os.makedirs(os.path.dirname(json_view_path), exist_ok=True)
    with open(print_version_path, "w") as f:
        json.dump(mcp_log['print_version'], f, indent=4)
    with open(json_view_path, "w") as f:
        json.dump(mcp_log['json_view'], f, indent=4)
    logger.info(f"Saved MCP logs to {print_version_path} and {json_view_path}")
    
    



