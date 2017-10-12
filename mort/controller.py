import logging
import time
from typing import List, Dict

from mort.download_utils import download_urls
from mort.driver import submit_request, get_job_state, is_done
from mort.imgdiff import get_similarity_index
from mort.repo_manager import extract_urls_from_job_details, local_dir_for_screen_shots, save_capture_result_to, \
    load_screenshots

logger = logging.getLogger(__name__)


def capture(paths: List[str], targets: List[Dict], git_hash: str):
    """
    Capture the screen shots for all the `paths` across all the OS and devices
    defined in `targets`.

    :param paths: List of all paths
    :param targets: List of all the targets
    :param git_hash: The hash of the current repo
    """
    logger.debug("Start capturing screen shots")
    logger.debug("- Paths: %s", paths)
    logger.debug("- Targets: %s", targets)

    results = {}
    for path in paths:
        logger.debug("Requesting screen shot for %s ...", path)
        job_id = submit_request(path, targets)
        while True:
            (job_is_completed, payload) = get_job_state(job_id)
            if job_is_completed:
                logger.info("Job %s is ready. ", job_id)
                results[path] = payload
                local_dir_for_screen_shots(job_id, git_hash)
                download_urls(extract_urls_from_job_details(payload), local_dir_for_screen_shots(job_id, git_hash))
            else:
                done_count = len(list(filter(is_done, payload['screenshots'])))
                logger.debug("Waiting [%d / %d]", done_count, len(targets))
                time.sleep(1)

    logger.info("All requests are completed. Saving everything to disk...")
    save_capture_result_to(results, git_hash)


def compare(paths: List[str], targets: List[Dict], curr_git_hash: str, ref_git_hash: str):
    screenshot_pairs = load_screenshots(paths, targets, curr_git_hash, ref_git_hash)
    for (path, target, curr_image_path, ref_image_path) in screenshot_pairs:
        diff_index = get_similarity_index(curr_image_path, ref_image_path)
        logger.debug("Image for %s + %s has similar index of %.2f", path, target, diff_index)

if __name__ == '__main__':
    from mort.local_conf import PATHS, TARGETS

    git_hash = '5e26d930'
    capture(PATHS, TARGETS, git_hash)
