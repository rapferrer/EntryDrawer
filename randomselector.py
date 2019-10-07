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
    """Object represents an individual in a competition with a number of entries"""
    def __init__(self, min, max, entries, name):
        self.min = min
        self.max = max
        self.entries = entries
        self.name = name

def main():
    args = takeInArgs()
    entrants = buildEntrants(args)

    if len(entrants) > 0:
        findWinningEntry(entrants)
    else:
        print("No entrants were entered!")
    exit(0)

def takeInArgs():
    parser = argparse.ArgumentParser(description='Lets randomly select an entry from a csv file...')
    parser.add_argument('file', type=str, help='The file/path to be used.')
    parser.add_argument('--no_header', action='store_true', help = 'Signal if there isn\'t a header line in the csv. Default is to assume that there is a header line')
    return parser.parse_args()

def buildEntrants(args):
    """Using the passed in args, build out and return an array of Entrant objects"""
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
                if not args.no_header and (line_count == 0):
                    line_count += 1
                else:
                    # Create the entrant object
                    try:
                        entries = int(row[1],10)
                        entrant = Entrant(minimum, minimum + entries, entries, row[0])
                        minimum = minimum + entries
                    except Exception as e: 
                        print("Expected a number but didn't get one after " + str(row[0]) + " in row " + str(line_count + 1))
                        print("{0}".format(e))
                        exit(2)
                    # Add them to the array
                    entrants.append(entrant)
                    line_count += 1
                    print(entrant.name + " has " + str(entrant.entries) + " entries")
                    print("There is currently a total of " + str(entrant.max) + " entries")
    return entrants

def findWinningEntry(entrants):
    """Takes in a list of Entrant objects, then finds a random entry in the list and selects it as the winner"""
    print("Time to select a random entry for our winner!")
    winningEntry = entrants[-1].max % random.randint(0, entrants[-1].max)
    print("Selecting entry number " + str(winningEntry))
    for entrant in entrants:
        if winningEntry < entrant.max:
            print("Our winner is " + (entrant).name)
            return

if __name__ == "__main__":
    main()
