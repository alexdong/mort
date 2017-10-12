from unittest import TestCase

from mort.list_utils import some, iterable, apply, all


def is_three(x):
    return x == 3


def is_multiple(x, y):
    return x % y == 0


class TestListUtils(TestCase):
    def test_all(self):
        self.assertFalse(all(is_three, [1, 2, 3]))
        self.assertTrue(all(is_three, [3, 3, 3]))

    def test_some(self):
        self.assertTrue(some(is_three, [1, 2, 3]))
        self.assertFalse(some(is_three, [1, 2, 4]))

        self.assertFalse(some(is_multiple, [(5, 3), (3, 2)]))
        self.assertTrue(some(is_multiple, [(4, 2), (3, 2)]))

    def test_iterable(self):
        self.assertTrue(iterable([]))
        self.assertTrue(iterable({}))
        self.assertFalse(iterable(1))

    def test_apply(self):
        self.assertFalse(apply(is_three, 1))
        self.assertTrue(apply(is_three, 3))
        self.assertTrue(apply(is_multiple, (4, 2)))
        self.assertFalse(apply(is_multiple, (3, 2)))
