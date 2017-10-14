from unittest import mock, TestCase

from mort.controller import capture, compare
from tests.data import PATH, TARGETS, JOB_ID, JOB_DETAIL, GIT_HASH_CURR, GIT_HASH_REF


class TestController(TestCase):
    @mock.patch('mort.controller.save_capture_result_to')
    @mock.patch('mort.controller.download_urls')
    @mock.patch('mort.controller.submit_request')
    @mock.patch('mort.controller.get_job_state')
    @mock.patch('time.sleep')
    def test_capture_successful(self, sleep, get_job_state, submit_request, download_urls, save_capture_result_to):
        submit_request.return_value = JOB_ID
        get_job_state.side_effect = [(False, JOB_DETAIL), (True, JOB_DETAIL)]
        download_urls.return_value = 1
        capture([PATH], [TARGETS[0]], GIT_HASH_CURR)
        self.assertEqual(download_urls.call_count, 1)
        self.assertEqual(submit_request.call_count, 1)
        self.assertEqual(get_job_state.call_count, 2)
        self.assertEqual(sleep.call_count, 1)
        self.assertEqual(save_capture_result_to.call_count, 1)

    @mock.patch('mort.controller.load_screenshots')
    @mock.patch('mort.controller.get_similarity_index')
    def test_compare(self, get_similarity_index, load_screenshots):
        load_screenshots.return_value = [('/', TARGETS[0], 'edited.jpg', 'original.jpg')]
        get_similarity_index.return_value = 0.95
        compare([PATH], TARGETS, GIT_HASH_CURR, GIT_HASH_REF)
        self.assertEqual(load_screenshots.call_count, 1)
        self.assertEqual(get_similarity_index.call_count, 1)
