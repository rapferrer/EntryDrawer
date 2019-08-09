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

def main(args):
    entries = []
    
    try:
        csv_file = open(str(args.file))
    except IOError as ioe:
        print("Pass in a correct file instead of causing:\n{0}".format(ioe))
    else:
        with csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            # Fill entries with counts
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    try:
                        entry = int(row[1],10)
                    except Exception as e: 
                        print("Expected a number but didn't get one after " + str(row[0]) + " in row " + str(line_count + 1))
                        print("{0}".format(e))
                        exit(2)
                    # we add row[1] number of entries into entries[] 
                    for count in range(entry):
                        entries.append(str(row[0]) + " " + str(count))
                    line_count += 1
                    print(row[0] + " " + str(len(entries)))
    
        print("Time to select a random entry!")
        winner = random.randint(0, len(entries))
        print("Selecting entry number " + str(winner))
        print("Our winner is " + entries[winner])
        exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lets randomly select an entry from a csv file...')
    parser.add_argument('file', type = str, help = 'The file/path to be used')
    args = parser.parse_args()
    main(args)
