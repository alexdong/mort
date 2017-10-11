from unittest import TestCase

from mort.target_matcher import matches, get_targets


class TestIsTarget(TestCase):
    TARGETS = [
        {"os": "ios", "os_version": "6.0", "device": "iPhone 4S (6.0)"},
        {"os": "Windows", "os_version": "XP", "browser": "ie", "browser_version": "7.0"},
        {"os": "Windows", "os_version": "XP", "browser": "chrome", "device": "", "browser_version": "47.0"},
        {"os": "Windows", "os_version": "XP", "browser": "chrome", "device": "", "browser_version": "48.0"},
        {"os": "Windows", "os_version": "XP", "browser": "chrome", "device": "", "browser_version": "49.0"}
    ]

    def test_single_match(self):
        self.assertTrue(matches(self.TARGETS[0], {"os": "ios"}))
        self.assertFalse(matches(self.TARGETS[0], {"os": "windows"}))
        self.assertFalse(matches(self.TARGETS[0], {"os": "windows", "browser_version": "10"}))

        self.assertFalse(matches(self.TARGETS[1], {"os": "ios"}))
        self.assertTrue(matches(self.TARGETS[1], {"os_version": "xp"}))
        self.assertTrue(matches(self.TARGETS[1], {"os_version": "xp", "browser": "ie"}))
        self.assertTrue(matches(self.TARGETS[1], {"os_version": "xp", "browser": "ie", "browser_version": "7"}))

    def test_match_against_target_list(self):
        self.assertGreaterEqual(len(get_targets({"device": "4s"})), 1)
        self.assertGreaterEqual(len(get_targets({"os": "win", "os_version": "xp", "browser": "chrome", "browser_version": "49"})), 1)
