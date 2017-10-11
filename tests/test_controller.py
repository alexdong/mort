from unittest import mock, TestCase

from mort.controller import capture
from tests.data import PATH, TARGETS, JOB_ID, JOB_DETAIL


class TestController(TestCase):
    @mock.patch('mort.controller.submit_request')
    @mock.patch('mort.controller.is_job_done')
    def test_capture(self, is_job_done, submit_request):
        submit_request.return_value = JOB_ID
        is_job_done.return_value = (True, JOB_DETAIL)
        result = capture([PATH], TARGETS)
        self.assertDictEqual(result[PATH], JOB_DETAIL)
