import csv
import random
import argparse

# This script takes in a csv file (that has a header) and randomly selects an entry from the total collected entries.
# The csv file should be in the following format:
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
    def __init__(self, min, max, entries, name):
        self.min = min
        self.max = max
        self.entries = entries
        self.name = name

def main(args):
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
                if line_count == 0:
                    line_count += 1
                else:
                    # Create the entrant object
                    try:
                        #entry = int(row[1],10)
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

        #TODO add call to findWinningEntry
        print("Our winner is " + findWinningEntry(entrants).name)
        exit(0)

def findWinningEntry(entrants):
    print("Time to select a random entry for our winner!")
    winningEntry = entrants[-1].max % random.randint(0, entrants[-1].max)
    print("Selecting entry number " + str(winningEntry))
    for entrant in entrants:
        if winningEntry < entrant.max:
            return entrant

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lets randomly select an entry from a csv file...')
    parser.add_argument('file', type = str, help = 'The file/path to be used')
    args = parser.parse_args()
    main(args)
