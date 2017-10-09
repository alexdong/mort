from unittest import mock, TestCase


class TestDriver(TestCase):
    @mock.patch('requests.post')
    @mock.patch('requests.get')
    def test_submit_request(self, get, post):
        pass
