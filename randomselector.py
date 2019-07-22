# This script takes in a csv file (that has a header) and is in the format:
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

def main():
    entries_file = None 
    try:
        entries_file = sys.argv[1]
    except:
        print("Give me something to work with here...")
        exit(1) 
    
    entries = []
    with open(str(entries_file)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # Fill entries with counts
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                try:
                    entry = int(row[1],10)
                except: 
                    print("Expected a number but didn't get one after " + str(row[0]) + " in row " + str(line_count + 1))
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
    import csv
    import random
    import sys
    main()
