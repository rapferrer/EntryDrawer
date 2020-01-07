#!/usr/bin/env python
"""Tests randomselector.py."""


import csv
import io
import random
import string
import unittest


class test_randomselector(unittest.TestCase):
    """Primary testing function."""

    @classmethod
    def setUpClass(self):
        """Set up the data that will be used in subsequent tests."""
        with io.StringIO() as output:
            writer = csv.writer(output, delimiter=',')
            writer.writerow(["entrant", "entries"])
            # Set up loop to generate n number of csv lines
            for x in range(10):
                randName = generate_random_entry_name()
                randEntries = random.randint(1, 300)
                writer.writerow([str(randName), str(randEntries)])
            csvFileContents = output.getvalue()
        self.csvFile = open("testFile", "w")
        self.csvFile.write(csvFileContents)

    def test_removeWinner(self):
        """Test the removeWinner() function."""


def generate_random_entry_name(size=6, chars=string.ascii_uppercase + string.digits):
    """Generate a random string that serves as an entrant name for testing."""
    return ''.join(random.choice(chars) for x in range(size))


if __name__ == "__main__":
    unittest.main()
