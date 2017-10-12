from unittest import mock, TestCase

import pytest

from mort.driver import submit_request, get_job_state, InvalidRequestError, \
    download_latest_target_list
from tests.data import PATH, TARGETS, JOB_ID, JOB_DETAIL


class TestSubmitRequest(TestCase):
    @mock.patch('requests.post')
    def test_submit_request_successful(self, post):
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.json = lambda: {'job_id': JOB_ID}
        post.return_value = resp
        job_id = submit_request(PATH, TARGETS)
        self.assertEqual(job_id, JOB_ID)
        self.assertEqual(post.call_count, 1)

    @mock.patch('requests.post')
    def test_submit_duplicated_request_returns_existing_job_id(self, post):
        resp = mock.MagicMock()
        resp.status_code = 422
        resp.json = lambda: {'job_id': JOB_ID}
        post.return_value = resp
        job_id = submit_request(PATH, TARGETS)
        self.assertEqual(job_id, JOB_ID)

    @mock.patch('requests.post')
    def test_submit_invalid_request_throws_out_exception(self, post):
        resp = mock.MagicMock()
        resp.status_code = 401
        post.return_value = resp
        with pytest.raises(InvalidRequestError):
            submit_request(PATH, TARGETS)


class TestWaitAndFetch(TestCase):
    @mock.patch('requests.get')
    def test_is_job_done(self, get):
        resp = mock.MagicMock()
        resp.json = lambda: {'state': 'all_queued', 'screenshots': []}
        get.return_value = resp
        is_job_completed, _ = get_job_state(JOB_ID)
        self.assertFalse(is_job_completed)

    @mock.patch('requests.get')
    def test_return_correct_list_when_ready(self, get):
        resp = mock.MagicMock()
        resp.json = lambda: JOB_DETAIL
        get.return_value = resp
        is_job_completed, response = get_job_state(JOB_ID)
        self.assertTrue(is_job_completed)
        self.assertIn('id', response)
        self.assertIn('screenshots', response)

    @mock.patch('requests.get')
    def test_download_latest_target_list(self, get):
        resp = mock.MagicMock()
        resp.content = b"abc"
        resp.json = lambda: [{}, {}]
        get.return_value = resp
        target_count = download_latest_target_list("/tmp/targets.json")
        self.assertEqual(2, target_count)
