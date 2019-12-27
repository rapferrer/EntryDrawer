#!/usr/bin/env python
"""Tests randomselector.py."""


import unittest
import randomselector


class test_randomselector(unittest.TestCase):
    """Primary testing function."""

    def setUpClass(cls):
        """Set up the data that will be used in subsequent tests."""
        cls._entrantsData = randomselector.buildEntrants(
            "../../sample-files/github-repos/entry-drawer/entriesTestData.txt")

    def test_removeWinner(cls):
        """Test the removeWinner() function."""


if __name__ == "__main__":
    unittest.main()
    print("Everything passed!")
