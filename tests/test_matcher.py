from unittest import TestCase

from tests.data import PATHS

from mort.matcher import path_in, target_matches, get_targets


class TestMatcher(TestCase):
    TARGETS = [
        {"os": "ios", "os_version": "6.0", "device": "iPhone 4S (6.0)"},
        {"os": "Windows", "os_version": "XP", "browser": "ie", "browser_version": "7.0"},
        {"os": "Windows", "os_version": "XP", "browser": "chrome", "device": "", "browser_version": "47.0"},
        {"os": "Windows", "os_version": "XP", "browser": "chrome", "device": "", "browser_version": "48.0"},
        {"os": "Windows", "os_version": "XP", "browser": "chrome", "device": "", "browser_version": "49.0"}
    ]

    def test_single_match(self):
        self.assertTrue(target_matches( {"os": "ios"}, self.TARGETS[0]))
        self.assertFalse(target_matches( {"os": "windows"}, self.TARGETS[0]))
        self.assertFalse(target_matches( {"os": "windows", "browser_version": "10"}, self.TARGETS[0]))

        self.assertFalse(target_matches( {"os": "ios"}, self.TARGETS[1]))
        self.assertTrue(target_matches( {"os_version": "xp"}, self.TARGETS[1]))
        self.assertTrue(target_matches( {"os_version": "xp", "browser": "ie"}, self.TARGETS[1]))
        self.assertTrue(target_matches( {"os_version": "xp", "browser": "ie", "browser_version": "7"}, self.TARGETS[1]))

    def test_match_against_target_list(self):
        self.assertGreaterEqual(len(get_targets({"device": "4s"})), 1)
        self.assertGreaterEqual(len(get_targets({"os": "win", "os_version": "xp", "browser": "chrome", "browser_version": "49"})), 1)

