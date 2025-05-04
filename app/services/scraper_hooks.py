import json
from browser_use import Agent
from browser_use.agent.views import AgentHistoryList
from typing import List, Tuple
import os
import logging
import base64

from app.utils.scraper_utils import save_to_pdf
import copy

logger = logging.getLogger(__name__)


async def save_page_content(agent: Agent) -> None:
    """Hook to save the page content at the end of the step if data was successfully scraped.

    Args:
        agent (_type_): _description_
    """
    # Make sure we have state history
    if hasattr(agent, "state"):
        history = agent.state.history
    else:
        history = None
        logging.warning("No state history found. Skipping page content saving.")
        return

    # Setup the results path + webpage number
    results_env = os.getenv("RESULTS_PATH")
    if not results_env:
        logging.error(
            "RESULTS_PATH environment variable is not set. Skipping page content saving."
        )
        return
    results_path = os.path.join(results_env, "local")
    trace_path = os.path.join(results_env, "trace")

    # get the current url and the number of urls scraped
    urls = agent.state.history.urls()
    current_url, step = urls[-1], len(urls)

    # Get the data from the trace file
    trace_json, updated_trace_json = initialize_trace_logging(
        history, trace_path, current_url, urls, step
    )
    webpage_number = updated_trace_json["url_to_webpage_number_mapper"][
        current_url
    ]  # Get the webpage number from the trace file (To keep consistent)

    # if current step is an error (example Ratelimit error), skip saving the page content
    if history.errors()[-1] is not None:
        logging.warning(
            f"Error detected in the current step: {history.errors()[-1]}. Skipping page content saving."
        )
        # still update the trace file with the error
        finalize_trace_logging(trace_path, step, None, None)
        return

    # Capture the cuurent page content
    browser_context = agent.browser_context
    website_html = await browser_context.get_page_html()
    website_screenshot = await browser_context.take_screenshot()
    website_screenshot = base64.b64decode(website_screenshot)
    page = await browser_context.get_current_page()

    webpage_file_path = False  # Initialize the webpage file path to False
    if not trace_json or current_url not in trace_json["urls"]:
        # If the current url has not been scraped before, save the page content
        logger.info(f"New Webpage detected: {current_url}. Saving content.")

        # create the new directory for the new webpage
        if not os.path.exists(f"{results_path}/webpage-{webpage_number}"):
            os.makedirs(f"{results_path}/webpage-{webpage_number}/")

        # save page as pdf
        await save_to_pdf(current_url, page, results_path, webpage_number)
        webpage_file_path = os.path.join(
            results_path, f"webpage-{webpage_number}", f"webpage-{webpage_number}.pdf"
        )

    # save the screenshot of the page with the current step number
    screenshot_path = os.path.join(
        results_path, f"webpage-{webpage_number}", f"screenshot-step-{step}.png"
    )
    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
    with open(screenshot_path, "wb") as f:
        f.write(website_screenshot)

    # Update trace again with some local path data
    finalize_trace_logging(trace_path, step, screenshot_path, webpage_file_path)

    return


def initialize_trace_logging(
    history: AgentHistoryList,
    trace_path: str,
    current_url: str,
    urls: List[str],
    step: int,
) -> Tuple[dict, dict]:
    """Handler to update file that traces the certain scraper actions

    Args:
        trace_path (_type_): _description_
    """
    FILENAME = "trace.json"

    # first check if the directory exists
    if not os.path.exists(trace_path):
        os.makedirs(trace_path)

    # check if the file exists
    if not os.path.exists(os.path.join(trace_path, FILENAME)):
        # create the file with an empty list
        with open(os.path.join(trace_path, FILENAME), "w") as f:
            f.write("{}")

    # Read and update the trace file with new data
    trace_file_path = os.path.join(trace_path, FILENAME)
    with open(trace_file_path, "r+") as f:
        try:
            # Load existing data or initialize an empty dictionary
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

        # Make a deep copy of the current trace to preserve the unmodified version
        current_trace = copy.deepcopy(data)

        #######################################################################
        # Update the trace
        #######################################################################
        # Add the current URL to the trace if it doesn't exist
        if "url_to_webpage_number_mapper" not in data:
            data["url_to_webpage_number_mapper"] = {current_url: 1}
        else:
            # if the current url not in the mapper, add it
            if current_url not in data["url_to_webpage_number_mapper"]:
                data["url_to_webpage_number_mapper"][current_url] = (
                    len(data["url_to_webpage_number_mapper"]) + 1
                )

        # Update the data with new URLs and current URL
        data["urls"] = list(set(urls))

        # Update the history during the current step
        if "history" not in data:
            data["history"] = {}

        if step not in data["history"]:
            data["history"][step] = {}

        data["history"][step]["action"] = (
            history.action_names() if history.action_names() else None
        )
        data["history"][step]["errors"] = (
            history.errors()[-1] if history.errors() else None
        )

        # Write the updated data back to the file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    # return the current trace and updated data
    return current_trace, data


def finalize_trace_logging(
    trace_path: str, step: int, screenshot_path: str, webpage_file_path: str
) -> None:
    """Handler to update file that traces the certain scraper actions

    Args:
        trace_path (_type_): _description_
    """
    FILENAME = "trace.json"

    # Read and update the trace file with new data
    trace_file_path = os.path.join(trace_path, FILENAME)
    with open(trace_file_path, "r+") as f:
        try:
            # Load existing data or initialize an empty dictionary
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

        #######################################################################
        # Update the trace
        #######################################################################

        # 'history' action should already exist in the trace file, so we just need to update it
        data["history"][str(step)]["screenshot_path"] = screenshot_path
        data["history"][str(step)]["webpage_file_path"] = (
            webpage_file_path
            if webpage_file_path
            else data["history"][str(step - 1)].get("webpage_file_path", None)
        )

        # Write the updated data back to the file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
