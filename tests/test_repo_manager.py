from unittest import TestCase

from mort.repo_manager import extract_urls_from_job_details, get_screenshot_path
from tests.data import JOB_ID, JOB_DETAIL, GIT_HASH_CURR


class TestRepoManager(TestCase):
    def test_extract_urls_from_job_details(self):
        urls = extract_urls_from_job_details(JOB_DETAIL)
        self.assertEqual(len(urls), 1)
        self.assertIn('android_Google-Nexus-6_5.0_portrait', urls[0])

    def test_get_screenshot_path(self):
        path = get_screenshot_path(GIT_HASH_CURR, JOB_DETAIL["screenshots"][0])
        self.assertIn(JOB_ID, path)
        self.assertIn("/fdd01e6683e0474ede370b753f870542f364f8ba/android_Google-Nexus-6_5.0_portrait.jpg", path)
