import os
import logging
import random

logger = logging.getLogger(__name__)


def setup_results_path(output_path: str, profile_name: str) -> str:
    """
    Set up the results path based on the provided output path and profile name.
    If the output path is not absolute, it will be resolved relative to the script location.
    """
    if not profile_name or not output_path:
        raise ValueError("Profile name and output path are required. Please provide valid values.")

    # check in the results path against all dirs that have the profile name in them ,append a 5 character random string to the end of the path
    random_string = os.urandom(5).hex()
    results_path = os.path.join(output_path, profile_name, random_string)
    while os.path.exists(results_path):
        random_string = os.urandom(5).hex()
        results_path = os.path.join(output_path, profile_name, random_string)
        
    # save the results path to the environment variable
    os.environ["RESULTS_PATH"] = results_path
    logger.info(f"Results will be saved to: {results_path}")