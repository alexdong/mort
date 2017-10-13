from unittest import mock, TestCase

from mort.file_utils import get_git_hash, create_dir_if_not_exists


class TestFileUtils(TestCase):
    @mock.patch('os.path.exists')
    @mock.patch('os.makedirs')
    def test_get_filename_from_url(self, makedirs, exists):
        exists.return_value = True
        create_dir_if_not_exists('/tmp/exist')
        self.assertEqual(exists.call_count, 1)
        self.assertEqual(makedirs.call_count, 0)

        exists.return_value = False
        create_dir_if_not_exists('/tmp/not-exist')
        self.assertEqual(exists.call_count, 2)
        self.assertEqual(makedirs.call_count, 1)

    @mock.patch("subprocess.check_output")
    def test_download(self, check_output):
        check_output.return_value = "34613b2".encode('utf-8')
        git_hash = get_git_hash()
        self.assertEqual(git_hash, "34613b2")
