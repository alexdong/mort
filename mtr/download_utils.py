import logging
import os
from functools import partial
from multiprocessing import Pool
from typing import List

import httplib2

logger = logging.getLogger(__name__)


def download_urls(urls: List[str], to_dir: str, pool_size: int = 16) -> int: # pragma: no cover
    """
    Download the specified urls to the specified dir and preserve the
    file's original name.

    :param urls: List of urls to JPEG or PNG images.
    :param to_dir: Full path to the directory where these files are saved into.
    :param pool_size: size of the worker pool for the downloader. Default is 16.
    :return: total number of images saved.
    """
    logger.debug("Download urls to %s: %s", to_dir, urls)
    with Pool(pool_size) as pool:
        pool.map(partial(download, to_dir=to_dir), urls)
    return len(urls)


def download(url: str, to_dir: str) -> str:
    """
    Download the remote url to local directory in the most memory efficient way.

    Since the Python 3.6.1 upgrade, `requests.get` will crash Python if
    when we try to run this function inside `multiprocessing.Pool`.
    Rewrite the logic in `httplib2` seems to make the issue go away.

    :param url: where the remote file is located.
    :param to_dir: the destination directory where the saved file will be stored
    :return: the full path to the newly downloaded file
    """
    to_file = os.path.join(to_dir, get_filename_from_url(url))
    logger.debug("Download %s to %s", url, to_file)
    create_dir_if_not_exist(to_dir)

    h = httplib2.Http(".cache")
    (_, content) = h.request(url, "GET")
    with open(to_file, 'wb') as f:
        f.write(content)
    return to_file


def create_dir_if_not_exist(dir: str) -> None:
    if not os.path.exists(dir):
        logger.debug("creating dir: %s", str)
        os.makedirs(dir)


def get_filename_from_url(url: str) -> str:
    return url.split('/')[-1]


# if __name__ == "__main__":
    # print(download("https://www.browserstack.com/screenshots/fdd01e6683e0474ede370b753f870542f364f8ba/android_Google-Nexus-6_5.0_portrait.jpg", "/tmp"))
    # print(download_urls(
    #     [
    #         "https://www.browserstack.com/screenshots/fdd01e6683e0474ede370b753f870542f364f8ba/android_Google-Nexus-6_5.0_portrait.jpg"],
    #     "/tmp"))
