from unittest import mock, TestCase

from mort.controller import capture
from tests.data import PATH, TARGETS, JOB_ID, JOB_DETAIL, GIT_HASH_CURR, GIT_HASH_REF


class TestController(TestCase):
    @mock.patch('mort.controller.download_urls')
    @mock.patch('mort.controller.submit_request')
    @mock.patch('mort.controller.is_job_done')
    def test_capture(self, is_job_done, submit_request, download_urls):
        submit_request.return_value = JOB_ID
        is_job_done.return_value = (True, JOB_DETAIL)
        download_urls.return_value = 1
        result = capture([PATH], TARGETS, GIT_HASH_CURR)
        self.assertDictEqual(result[PATH], JOB_DETAIL)
        self.assertEqual(download_urls.call_count, 1)
