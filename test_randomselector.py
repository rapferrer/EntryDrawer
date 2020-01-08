#!/usr/bin/env python
"""Tests randomselector.py."""


import csv
import io
import os
import random
import randomselector
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
            testEntrantNames = ['Bojack', 'Carolyn', 'Todd', 'Sarah', 'Peanutbutter', 'Diane',
                                'Pinky', 'Herb', 'Butterscotch', 'Beatrice']
            for name in testEntrantNames:
                randEntries = random.randint(1, 300)
                writer.writerow([name, str(randEntries)])
            csvFileContents = output.getvalue()
        csvFile = open("testFile.csv", "w")
        with csvFile:
            csvFile.write(csvFileContents)
        self.entrants = randomselector.buildEntrants(fileName="testFile.csv")

    @classmethod
    def tearDownClass(self):
        """Remove created file."""
        os.remove("testFile.csv")

    def test_isUnique(self):
        """Test the isUnique() function."""
        randKey = random.randint(1, len(self.entrants))
        name = self.entrants[randKey]
        self.assertTrue(randomselector.isUnique(name, self.entrants))

    def test_selectWinner(self):
        """Test the selectWinner() function."""
        winner = randomselector.selectWinner(self.entrants)
        self.assertTrue(winner in self.entrants)

    def test_removeWinner(self):
        """Test the removeWinner() function."""
        randKey = random.randint(1, len(self.entrants))
        randEntrant = self.entrants[randKey]
        self.assertTrue(randEntrant not in randomselector.removeWinner(self.entrants, randEntrant))


def generate_random_entry_name(size=6, chars=string.ascii_uppercase + string.digits):
    """Generate a random string that serves as an entrant name for testing."""
    return ''.join(random.choice(chars) for x in range(size))


if __name__ == "__main__":
    unittest.main()
