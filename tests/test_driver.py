from unittest import mock, TestCase

import pytest

from mtr.driver import submit_request, wait_and_fetch_all_urls, InvalidRequestError, download_latest_target_list


class TestSubmitRequest(TestCase):
    PATH = "/products/collage-posters"
    TARGETS = [
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
    JOB_ID = 'fdd01e6683e0474ede370b753f870542f364f8ba'

    @mock.patch('requests.post')
    def test_submit_request_successful(self, post):
        resp = mock.MagicMock()
        resp.status_code = 200
        resp.json = lambda: {'job_id': self.JOB_ID}
        post.return_value = resp
        job_id = submit_request(self.PATH, self.TARGETS)
        self.assertEqual(job_id, self.JOB_ID)
        self.assertEqual(post.call_count, 1)

    @mock.patch('requests.post')
    def test_submit_duplicated_request_returns_existing_job_id(self, post):
        resp = mock.MagicMock()
        resp.status_code = 422
        resp.json = lambda: {'job_id': self.JOB_ID}
        post.return_value = resp
        job_id = submit_request(self.PATH, self.TARGETS)
        self.assertEqual(job_id, self.JOB_ID)

    @mock.patch('requests.post')
    def test_submit_invalid_request_throws_out_exception(self, _):
        resp = mock.MagicMock()
        resp.status_code = 401
        with pytest.raises(InvalidRequestError):
            submit_request(self.PATH, self.TARGETS)


class TestWaitAndFetch(TestCase):
    JOB_ID = 'fdd01e6683e0474ede370b753f870542f364f8ba'

    @mock.patch('requests.get')
    @mock.patch('time.sleep')
    def test_sleep_if_not_ready(self, sleep, get):
        resp = mock.MagicMock()
        resp.json = lambda: {'state': 'all_queued'}
        get.return_value = resp
        urls = wait_and_fetch_all_urls(self.JOB_ID, 1)
        self.assertEqual(urls, [])
        self.assertEqual(sleep.call_count, 1)

    @mock.patch('requests.get')
    @mock.patch('time.sleep')
    def test_return_correct_list_when_ready(self, sleep, get):
        resp = mock.MagicMock()
        resp.json = lambda: {
            "id": "fdd01e6683e0474ede370b753f870542f364f8ba",
            "state": "done",
            "callback_url": None,
            "win_res": "1024x768",
            "mac_res": "1024x768",
            "quality": "compressed",
            "wait_time": 5,
            "orientation": "portrait",
            "screenshots": [
                {"browser": "Android Browser",
                 "browser_version": "",
                 "os": "android",
                 "os_version": "5.0",
                 "device": "Google Nexus 6",
                 "image_url": "https://www.browserstack.com/screenshots/fdd01e6683e0474ede370b753f870542f364f8ba/android_Google-Nexus-6_5.0_portrait.jpg",
                 "thumb_url": "https://www.browserstack.com/screenshots/fdd01e6683e0474ede370b753f870542f364f8ba/thumb_android_Google-Nexus-6_5.0_portrait.jpg",
                 "state": "done",
                 "url": "https://staging.happymoose.nz/products/collage-posters",
                 "orientation": None,
                 "id": "d557ed648e109ac1d947db78f7693f3ef76a883b",
                 "created_at": "2017-10-09 21:41:07 UTC"},
            ]}
        get.return_value = resp
        urls = wait_and_fetch_all_urls(self.JOB_ID)
        self.assertEqual(sleep.call_count, 0)
        self.assertEqual(len(urls), 1)
        self.assertIn('android_Google-Nexus-6_5.0_portrait', urls[0])

    @mock.patch('requests.get')
    def test_download_latest_target_list(self, get):
        resp = mock.MagicMock()
        resp.content = b"abc"
        resp.json = lambda: [{}, {}]
        get.return_value = resp
        target_count = download_latest_target_list("/tmp/targets.json")
        self.assertEqual(2, target_count)
