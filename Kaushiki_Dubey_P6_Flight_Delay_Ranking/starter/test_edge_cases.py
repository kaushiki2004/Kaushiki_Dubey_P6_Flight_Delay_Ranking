"""Focused correctness and stability tests for all four techniques."""

import unittest

from my_solutions import TECHNIQUES


def instance(delays):
    ids = [f"F{i}" for i in range(len(delays))]
    return {"n": len(ids), "ids": ids, "delay": delays}


class FlightRankingTests(unittest.TestCase):
    def assert_all_methods(self, delays, expected):
        for name, technique in TECHNIQUES.items():
            with self.subTest(technique=name):
                self.assertEqual(technique(instance(delays)), expected)

    def test_empty_file(self):
        self.assert_all_methods([], [])

    def test_single_flight(self):
        self.assert_all_methods([12], ["F0"])

    def test_equal_delays_keep_file_order(self):
        self.assert_all_methods([7, 7, 7, 7], ["F0", "F1", "F2", "F3"])

    def test_negative_and_positive_delays(self):
        self.assert_all_methods([-60, 0, 900, -1], ["F2", "F1", "F3", "F0"])

    def test_duplicate_delays_are_stable(self):
        self.assert_all_methods([5, 20, 5, 20, 5], ["F1", "F3", "F0", "F2", "F4"])

    def test_already_ranked(self):
        self.assert_all_methods([9, 4, 4, -2], ["F0", "F1", "F2", "F3"])

    def test_reverse_ranked(self):
        self.assert_all_methods([-2, 4, 4, 9], ["F3", "F1", "F2", "F0"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
