import json
from functools import partial
import logging
import os
from typing import List, Dict, Optional, Tuple

from mort.local_conf import SCREEN_SHOT_SAVED_TO
from mort.matcher import target_matches
from mort.list_utils import first

logger = logging.getLogger(__name__)


def extract_urls_from_job_details(job_detail: Dict) -> List[str]:
    """ Extract the screenshot urls from BrowserStack's `/screenshots/${JOB_ID}.json}` response """
    return [screenshot['image_url'] for screenshot in job_detail['screenshots'] if screenshot['image_url']]


def local_dir_for_screen_shots(job_id: str, git_hash: str) -> str:
    """ Get the full path to save the individual screen shots for the given `git_hash` """
    return os.path.join(SCREEN_SHOT_SAVED_TO, git_hash, job_id)


def save_capture_result_to(capture_result: Dict, git_hash: str) -> str:
    """ Save the capture result into repo for the given `git_hash`. """
    manifest_file_path = os.path.join(SCREEN_SHOT_SAVED_TO, git_hash, "manifest.json")
    with open(manifest_file_path, 'w') as fp:
        fp.write(json.dumps(capture_result, indent=4, sort_keys=True))
    return manifest_file_path


def get_screenshot_path(git_hash: str, screenshot: Dict) -> str:
    """ Return the full path to the screenshot image on disk for given `git_hash` """
    return os.path.join(SCREEN_SHOT_SAVED_TO, git_hash,
                        '/'.join(screenshot['image_url'].split('/')[-2:]))


def create_repo(git_hash: str, job_id: str):
    path = os.path.join(SCREEN_SHOT_SAVED_TO, git_hash, job_id)
    if not os.path.exists(path):
        logger.debug("creating repo dir for %s, %s", git_hash, job_id)
        os.makedirs(path)


def load_screenshots(paths: List[str], targets: List[Dict], curr_git_hash: str, ref_git_hash: str) -> List[Tuple]:
    """
    Load all screenshots for the given `git_hash`, filtered them by `paths` and `targets`,
    and return a list of tuples of `(path, target, curr screenshot path, reference screenshot path)`
    """
    results: List[Tuple] = []
    for path in paths:
        for target in targets:
            curr_screenshot = get_screenshot(curr_git_hash, path, target)
            ref_screenshot = get_screenshot(ref_git_hash, path, target)
            if not curr_screenshot or not ref_screenshot:
                continue

            curr_path = get_screenshot_path(curr_git_hash, curr_screenshot)
            ref_path = get_screenshot_path(ref_git_hash, ref_screenshot)
            results.append((path, target, curr_path, ref_path))

    return results


def get_screenshot(git_hash: str, path: str, target_spec: Dict) -> Optional[Dict]:
    """ Get the a specific screen shot details given git_hash, path and
    target specification. Return None if nothing is found. """
    manifest_file_path = os.path.join(SCREEN_SHOT_SAVED_TO, git_hash, "manifest.json")
    manifest = json.loads(open(manifest_file_path, 'r').read())
    return first(partial(target_matches, target_spec), manifest[path])
