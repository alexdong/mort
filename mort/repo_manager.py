import json
import logging
import os
from typing import List, Dict, Optional, Tuple

from mort.local_conf import SCREEN_SHOT_SAVED_TO
from mort.matcher import target_matches

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


def load_manifest_for(git_hash: str) -> Dict:
    manifest_file_path = os.path.join(SCREEN_SHOT_SAVED_TO, git_hash, "manifest.json")
    return json.loads(open(manifest_file_path, 'r').read())


def create_repo(git_hash: str, job_id: str):
    path = os.path.join(SCREEN_SHOT_SAVED_TO, git_hash, job_id)
    if not os.path.exists(path):
        logger.debug("creating repo dir for %s, %s", git_hash, job_id)
        os.makedirs(path)


def find_all_screenshots(git_hash: str, paths: List[str], targets: List[Dict]) -> List[Tuple]:
    """
    Load all screenshots for the given `git_hash`, filtered them by `paths` and `targets`,
    and return a list of tuples of `(path, target, screenshot_file_path)`
    """
    manifest = load_manifest_for(git_hash)
    results: List[Tuple] = []

    candidates = [(path, screenshots) for (path, screenshots) in manifest.items() if path in paths]
    for path, screenshots in candidates:
        for screenshot in screenshots:
            if not target_matches(screenshot, targets):
                continue

            screenshot_path = get_screenshot_path(git_hash, screenshot)
            results.append((path, screenshot, screenshot_path))

    return results


def find_screenshot(git_hash: str, path: str, target: Dict) -> Optional[str]:
    manifest = load_manifest_for(git_hash)
    for screenshot in manifest[path]:
        if target_matches(screenshot, target):
            return get_screenshot_path(git_hash, screenshot)
    return None
