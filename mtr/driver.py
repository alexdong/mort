import json
import logging
from typing import List, Dict

import requests

from mtr.local_conf import BROWSER_STACK_ACCESS_KEY, SERVER

logger = logging.getLogger(__name__)


def request_single_screenshot(path: str, targets: List[Dict]) -> List[str]:
    """
    Request a set of screenshots to be generated for the specified `url` on `targets` devices.

    We first send a POST request to `POST /screenshots`, which will send back a `job_id`;
    we'll then start polling the endpoint `GET /screenshots/<JOB-ID>.json`.
    Please note that this method blocks the caller.

    :param path: path to the web page we are testing. For example: `"/products/collage-posters"`
    :param targets: a list of target OS and browser "descriptors". For example: [
            {
                "os": "Windows",
                "os_version": "XP",
                "browser": "ie",
                "browser_version": "7.0"
            },
            {
                "os": "ios",
                "os_version": "6.0",
                "device": "iPhone 4S (6.0)"
            }
        ]
    :return: list of the urls to download the full page png files. For example: [
        "https://www.browserstack.com/screenshots/13b93a14db22872fcb5fd1c86b730a51197db319/winxp_ie_7.0.png",
        "https://www.browserstack.com/screenshots/13b93a14db22872fcb5fd1c86b730a51197db319/win7_ie_8.0.png"]
    """
    # Request the screen shots
    request_payload = {"url": SERVER + path, "browsers": targets}
    headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    logger.debug("Sending screen shot requests: {0}".format(request_payload))
    r = requests.post('https://www.browserstack.com/screenshots', data=json.dumps(request_payload),
                      headers=headers, auth=BROWSER_STACK_ACCESS_KEY)
    if r.status_code is not 200:
        logger.error("BrowserStack.com returns error code: {0}".format(r.status_code))
        if r.status_code == 422 and 'job_id' in r.json():
            job_id = r.json()['job_id']
        else:
            logger.error("invalid request: {0}".format(r.content))
            return []

    # Pull out the job id and start polling
    job_id = r.json()['job_id']
    logger.info("job id: {0}".format(job_id))

    # Get grab all the links
    r = requests.get('https://www.browserstack.com/' + job_id + '.json', auth=BROWSER_STACK_ACCESS_KEY)
    logger.debug("Job returns: {0}".format(r.status_code))
    logger.debug("    payload: {0}".format(r.content))
    return [screenshot['image_url'] for screenshot in r.json()['screenshots']]


if __name__ == "__main__":
    print(request_single_screenshot("/products/sleek-boards", [
        {
            "os": "android",
            "os_version": "5.0",
            "browser": "Android Browser",
            "device": "Google Nexus 6",
            "browser_version": "",
        },
        {
            "os": "ios",
            "os_version": "7.0",
            "browser": "Mobile Safari",
            "device": "iPhone 5S",
            "browser_version": "",
        },
        {
            "os": "Windows",
            "os_version": "10",
            "browser": "edge",
            "device": "",
            "browser_version": "14.0",
        },
        {
            "os": "OS X",
            "os_version": "Yosemite",
            "browser": "chrome",
            "device": "",
            "browser_version": "50.0",
        },
    ]))
