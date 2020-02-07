#!/usr/bin/env python
"""Takes in a list of entrants from a .csv and finds the winner or winners."""

import csv
import random
import argparse
import json

# This script takes in a csv or json file and randomly selects an entry from the total collected
# entries.
#
# The csv file doesn't have to have a header row, but the assumed format of the .csv file is:
#
# Name, Entries
# Ryan P., 23
# ...
#
# The assumed format of the .json file is:
#
# {
#    "entrants" : [
#        {
#            "name" : "Ryan P.",
#            "entries" : 37
#        },
#        ...
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
    if args.json:
        entrants = buildEntrantsJson(args)
    else:
        entrants = buildEntrantsTxt(args)

    if len(entrants) > 0:
        if args.without_removal:
            findWinningEntriesWithoutRemoval(entrants, args.number_of_winners)
        else:
            findWinningEntriesWithRemoval(entrants, args.number_of_winners)
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
    parser.add_argument('--without_removal', action='store_true', help='Choose multiple winners\
         without removing the winners from the list of entrants. Default is false')
    parser.add_argument('-q', '--quiet', action='store_true', help='Print less to stdout')
    parser.add_argument('-j', '--json', action='store_true', help='Read entries from a JSON file')
    return parser.parse_args()


def buildEntrantsTxt(args):
    """Use the passed in args to build out and return an array of Entrant objects from a .txt
    file."""
    entrants = []
    try:
        csv_file = open(str(args.file))
    except IOError as ioe:
        print("Pass in a correct file instead of causing:\n{0}".format(ioe))
    else:
        with csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            minimum = 0
            for row in csv_reader:
                if (line_count == 0) and not args.no_header:
                    line_count += 1
                else:
                    # Create the entrant object
                    try:
                        line_count += 1
                        strippedName = row[0].strip()
                        if not isUnique(strippedName, entrants):
                            continue
                        entries = int(row[1], 10)
                        entrant = Entrant(minimum, minimum + entries, entries, strippedName)
                        minimum = minimum + entries
                    except ValueError as ve:
                        # Catches non-integer characters/sequences
                        print("\nOops! Expected an integer (whole number) but didn't get one "
                              "after " + str(row[0]) + " in row " + str(line_count))
                        print("ValueError: {0}\n".format(ve))
                        continue
                    except IndexError as ie:
                        # Catches emtpy lines
                        print("\nOops! Expected info on line " + str(line_count) + " but found "
                              "nothing!")
                        print("IndexError: {0}\n".format(ie))
                        continue
                    entrants.append(entrant)
                    if not args.quiet:
                        print(entrant.name + " has " + str(entrant.entries) + " entries")
                        print("There is currently a total of " + str(entrant.max) + " entries")
    return entrants


def buildEntrantsJson(args=None):
    """Use the passed in args to build out and return an array of Entrant objects from a .json
    file."""
    entrants = []
    try:
        jsonFile = open(str(args.file))
    except IOError as ioe:
        print("Pass in a correct file instead of causing:\n{0}".format(ioe))
    else:
        with jsonFile:
            minimum = 0
            data = json.load(jsonFile)
            for jsonObject in data['entrants']:
                # Create the entrant object
                try:
                    name = jsonObject['name']
                    if not isUnique(name, entrants):
                        continue
                    entries = int(jsonObject['entries'])
                    entrant = Entrant(minimum, minimum + entries, entries, name)
                    minimum = minimum + entries
                except ValueError as ve:
                    # Catches non-integer characters/sequences
                    print("\nOops! Expected an integer (whole number) but didn't get one "
                          "with " + name)
                    print("ValueError: {0}\n".format(ve))
                    continue
                entrants.append(entrant)
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


def findWinningEntry(entrants, withRemoval):
    """Take in a list of Entrant objects, then find a random entry in the list and selects it as\
    the winner."""
    print("Time to select a random entry for our winner!")
    winningEntry = entrants[-1].max % random.randint(0, entrants[-1].max)
    print("Selecting entry number " + str(winningEntry))
    for entrant in entrants:
        if winningEntry < entrant.max:
            if withRemoval:
                print("Our winner is " + (entrant).name)
            return entrant


def findWinningEntriesWithRemoval(entrants, numberOfWinners):
    """Find x winning entries from the list of entrants(x being the second arg passed in)."""
    winner = findWinningEntry(entrants, True)
    if (numberOfWinners > 1):
        reducedEntrants = removeWinner(entrants, winner)
        findWinningEntriesWithRemoval(reducedEntrants, numberOfWinners - 1)
    return winner


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


def findWinningEntriesWithoutRemoval(entrants, numberOfWinners):
    """Find winners in the entrants list without removing them from the list as they are\
    selected."""
    winnerEntrants = []
    x = 0
    while x < numberOfWinners:
        winner = findWinningEntry(entrants, False)
        if winner not in winnerEntrants:
            winnerEntrants.append(winner)
            x += 1
        else:
            print("Oops. We selected " + winner.name + " a second time! Drawing again!")
    printWinners(winnerEntrants)
    return


def printWinners(winners):
    """Print a list of Entrant objects."""
    print("Here are our winners!")
    for winner in winners:
        print(winner.name)
    return


if __name__ == "__main__":
    main()
