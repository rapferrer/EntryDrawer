#!/usr/bin/env python
"""Takes in a list of entrants from a .csv and finds the winner or winners."""

import csv
import random
import argparse

# This script takes in a csv file and randomly selects an entry from the total collected entries.
# The csv file doesn't have to have a header row, but the assumed format of the .csv file is:
#
# *header row*
# entrant1, entrant 1's number of entries
# entrant2, entrant 2's number of entries
# etc...
#
# ex.
# Name, Entries
# Ryan, 23
# Chad, 45
# Katherine, 117
# ...
#


class Entrant:
    """Object represents an individual in a competition with a number of entries."""

    def __init__(self, min, max, entries, name):
        """Define the Entrant class."""
        self.min = min
        self.max = max
        self.entries = entries
        self.name = name


def main():
    """Acts as the overall controller of the script."""
    args = takeInArgs()
    entrants = buildEntrants(args)
    winners = []

    if len(entrants) > 0:
        for x in range(args.number_of_winners):
            selectedWinner = selectWinner(entrants)
            winners.append(selectedWinner)
            entrants = removeWinner(entrants, selectedWinner)
        printWinners(winners)
    else:
        print("No entrants were entered!")
    exit(0)


def takeInArgs():
    """Take in arguments from the command line."""
    parser = argparse.ArgumentParser(description='Lets randomly select an entry from a csv file...')
    parser.add_argument('file', type=str, help='The file/path to be used.')
    parser.add_argument('--no_header', action='store_true', help='Signal if there isn\'t a header\
     line in the csv. Default is to assume that there is a header line')
    parser.add_argument('--number_of_winners', type=int, default=1, help='The number of winners to\
     select. Default is 1')
    parser.add_argument('-q', '--quiet', action='store_true', help='Print less to stdout')
    return parser.parse_args()


def buildEntrants(args=None, fileName=None):
    """Use the passed in args to build out and return an array of Entrant objects."""
    entrants = []
    try:
        if args is not None:
            csvFile = open(str(args.file))
        else:
            csvFile = open(str(fileName))
    except IOError as ioe:
        print("Pass in a correct file instead of causing:\n{0}".format(ioe))
    else:
        with csvFile:
            csv_reader = csv.reader(csvFile, delimiter=',')
            line_count = 0
            minimum = 0
            for row in csv_reader:
                if args is not None:
                    if (line_count == 0) and not args.no_header:
                        line_count += 1
                        continue
                elif args is None and line_count == 0:
                    line_count += 1
                    continue
                # Create the entrant object
                try:
                    strippedName = row[0].strip()
                    if not isUnique(strippedName, entrants):
                        continue
                    entries = int(row[1], 10)
                    entrant = Entrant(minimum, minimum + entries, entries, strippedName)
                    minimum = minimum + entries
                except ValueError as ve:
                    # Catches non-integer characters/sequences
                    print("\nOops! Expected an integer (whole number) but didn't get one "
                          "after " + str(row[0]) + " in row " + str(line_count + 1))
                    print("ValueError: {0}\n".format(ve))
                    continue
                except IndexError as ie:
                    # Catches emtpy lines
                    print("\nOops! Expected info on line " + str(line_count + 1) + " but found "
                          "nothing!")
                    print("IndexError: {0}\n".format(ie))
                    continue
                entrants.append(entrant)
                line_count += 1
                if args is not None:
                    if not args.quiet:
                        print(entrant.name + " has " + str(entrant.entries) + " entries")
                        print("There is currently a total of " + str(entrant.max) + " entries")
    return entrants


def isUnique(name, entrants):
    """Check to see if a name already belongs to an entrant in the list of entrants."""
    unique = True
    for existingEntrant in entrants:
        if name == existingEntrant.name:
            print(name + " already exists! Skipping")
            unique = False
            break
    return unique


def selectWinner(entrants):
    """Select a winner at random from the passed in entrants."""
    winningEntry = entrants[-1].max % random.randint(0, entrants[-1].max)
    for entrant in entrants:
        if winningEntry < entrant.max:
            return entrant


def removeWinner(entrants, winner):
    """Return a list of Entrant objects minus the passed in Entrant."""
    entrants.remove(winner)

    # Reset the min/max values of the remaining entrant objects
    minimum = 0
    for entrant in entrants:
        if minimum != entrant.min:
            entrant.min = minimum
            entrant.max = minimum + entrant.entries
        minimum = entrant.max
    return entrants


def printWinners(winners):
    """Print a list of Entrant objects."""
    print("Here are our winners!")
    for winner in winners:
        print(winner.name)
    return


if __name__ == "__main__":
    main()
