from unittest import TestCase

from mort.list_utils import some, iterable, apply


def is_three(x):
    return x == 3


def is_multiple(x, y):
    return x % y == 0


class TestListUtils(TestCase):
    def test_some(self):
        self.assertTrue(some([1, 2, 3], is_three))
        self.assertFalse(some([1, 2, 4], is_three))

        self.assertFalse(some([(5, 3), (3, 2)], is_multiple))
        self.assertTrue(some([(4, 2), (3, 2)], is_multiple))

    def test_iterable(self):
        self.assertTrue(iterable([]))
        self.assertTrue(iterable({}))
        self.assertFalse(iterable(1))

    def test_apply(self):
        self.assertFalse(apply(is_three, 1))
        self.assertTrue(apply(is_three, 3))
        self.assertTrue(apply(is_multiple, (4, 2)))
        self.assertFalse(apply(is_multiple, (3, 2)))
