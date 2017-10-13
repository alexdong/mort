from unittest import TestCase

from mort.imgdiff import get_similarity_index, generate_annotated_diff_image
from tests.data import get_absolute_path


class TestImageDiff(TestCase):
    ORIGIN = get_absolute_path('tests/resources/origin.png')
    EDITED = get_absolute_path('tests/resources/edited.png')

    def test_get_similarity_index(self):
        index = get_similarity_index(self.EDITED, self.ORIGIN)
        self.assertLess(index, 1)
        self.assertGreater(index, 0)

    def test_generate_diff_image(self):
        diff_count = generate_annotated_diff_image(self.EDITED, self.ORIGIN, '/tmp/diff.png')
        self.assertEqual(diff_count, 1)
