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
    return parser.parse_args()


def buildEntrants(args):
    """Use the passed in args to build out and return an array of Entrant objects."""
    entrants = []
    try:
        csv_file = open(str(args.file))
    except IOError as ioe:
        print("Pass in a correct file instead of causing:\n{0}".format(ioe))
    else:
        with csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            # Fill entries with counts
            minimum = 0
            for row in csv_reader:
                if (line_count == 0) and not args.no_header:
                    line_count += 1
                else:
                    # Create the entrant object
                    try:
                        strippedName = row[0].strip()
                        if not isUnique(strippedName, entrants):
                            continue
                        entries = int(row[1], 10)
                        entrant = Entrant(minimum, minimum + entries, entries, strippedName)
                        minimum = minimum + entries
                    except Exception as e:
                        print("\nOops! Expected a number but didn't get one after " +
                              str(row[0]) + " in row " + str(line_count + 1))
                        print("Error: {0}\n".format(e))
                        continue
                    # Add them to the array
                    entrants.append(entrant)
                    line_count += 1
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
