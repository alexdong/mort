from unittest import mock, TestCase

from mort.download_utils import get_filename_from_url, download, create_dir_if_not_exist


class TestUtils(TestCase):
    URL = "https://www.browserstack.com/screenshots/fdd01e6683e0474ede370b753f870542f364f8ba/" + \
          "android_Google-Nexus-6_5.0_portrait.jpg"

    def test_get_filename_from_url(self):
        self.assertEqual(
            "android_Google-Nexus-6_5.0_portrait.jpg", get_filename_from_url(self.URL))

    @mock.patch("httplib2.Http.request")
    @mock.patch('mort.download_utils.create_dir_if_not_exist')
    def test_download(self, create_dir, request):
        request.return_value = (None, b"abc")
        file_path = download(self.URL, "/tmp")
        self.assertEqual("/tmp/android_Google-Nexus-6_5.0_portrait.jpg", file_path)
        self.assertEqual(create_dir.call_count, 1)

    @mock.patch('os.makedirs')
    def test_create_dir(self, makedirs):
        create_dir_if_not_exist("/tmp/this-does-not-exist")
        self.assertEqual(makedirs.call_count, 1)
