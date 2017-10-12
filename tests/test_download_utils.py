from unittest import mock, TestCase

from mort.download_utils import get_filename_from_url, download


class TestUtils(TestCase):
    URL = "https://www.browserstack.com/screenshots/fdd01e6683e0474ede370b753f870542f364f8ba/" + \
          "android_Google-Nexus-6_5.0_portrait.jpg"

    def test_get_filename_from_url(self):
        self.assertEqual(
            "android_Google-Nexus-6_5.0_portrait.jpg", get_filename_from_url(self.URL))

    @mock.patch("httplib2.Http.request")
    def test_download(self, request):
        request.return_value = (None, b"abc")
        file_path = download(self.URL, "/tmp")
        self.assertEqual("/tmp/android_Google-Nexus-6_5.0_portrait.jpg", file_path)
