import logging
import os
from typing import List, Dict

from mort.download_utils import download_urls
from mort.driver import submit_request, is_job_done
from mort.local_conf import SCREEN_SHOT_SAVED_TO
from mort.repo_manager import extract_urls_from_job_details

logger = logging.getLogger(__name__)


def capture(paths: List[str], targets: List[Dict], git_hash: str) -> Dict:
    """
    Capture the screen shots for all the `paths` across all the OS and devices
    defined in `targets`.

    :param paths: List of all paths
    :param targets: List of all the targets
    :param git_hash: The hash of the current repo
    :return: A dict where each key is the path and the value BrowserStack's response
    """
    logger.debug("Start capturing screen shots")
    logger.debug("- Paths: %s", paths)
    logger.debug("- Targets: %s", targets)

    path_to_response_map: Dict[str, Dict] = dict([(path, {}) for path in paths])
    job_id_to_path_map: Dict[str, str] = dict([(submit_request(path, targets), path) for path in paths])
    job_queue: List[str] = list(job_id_to_path_map.keys())
    logger.info("All requests are queued. Now, waiting for them to get ready ...")

    # Loop through the job_id in the `job_queue`, if the job is completed,
    # save the response into `path_to_response_map` and then remove it from the queue.
    # We use a little bit Python trick here to modify the job_queue while iterating it.
    # This techinque is best described in https://stackoverflow.com/a/1207427/128601
    # This is the reason why we
    # 1. `job_queue = list(...)`: convert `DictKeys` object into a list where `[:]` is possible
    # 2. `job_queue[:]`: to loop and modify it at the same time
    for job_id in job_queue[:]:  # [:]
        path = job_id_to_path_map[job_id]
        logger.debug("Checking job %s status for path %s", job_id, path)
        (job_is_completed, payload) = is_job_done(job_id)
        if job_is_completed:
            path_to_response_map[path] = payload

            download_to_dir = os.path.join(SCREEN_SHOT_SAVED_TO, git_hash, job_id)
            logger.info("Job %s is ready. Now downloading all images to %s", job_id, download_to_dir)
            download_urls(extract_urls_from_job_details(payload), download_to_dir)

            job_queue.remove(job_id)
            logger.info("Job %s is ready, %d left in the queue", job_id, len(job_queue))

    return path_to_response_map
