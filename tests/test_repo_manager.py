from unittest import TestCase

from mort.repo_manager import extract_urls_from_job_details
from tests.data import JOB_DETAIL


class TestRepoManager(TestCase):
    def test_extract_urls_from_job_details(self):
        urls = extract_urls_from_job_details(JOB_DETAIL)
        self.assertEqual(len(urls), 1)
        self.assertIn('android_Google-Nexus-6_5.0_portrait', urls[0])
