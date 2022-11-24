#!/usr/bin/env python

import logging

from argparse import ArgumentParser
from randomselector import (
    buildEntrants,
    findWinningEntriesWithoutRemoval,
    findWinningEntriesWithRemoval
)


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

logger = logging.getLogger(__name__)


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
        logging.info(f'No entrants were entered!')
    exit(0)


def takeInArgs():
    """Take in arguments from the command line."""
    parser = ArgumentParser(description='Lets randomly select an entry from a csv file...')
    parser.add_argument('file', type=str, help='The file/path to be used.')
    parser.add_argument('--no_header', action='store_true', help='Signal if there isn\'t a header\
     line in the csv. Default is to assume that there is a header line')
    parser.add_argument('--number_of_winners', type=int, default=1, help='The number of winners to\
     select. Default is 1')
    parser.add_argument('--without_removal', action='store_true', help='Choose multiple winners\
         without removing the winners from the list of entrants. Default is false')
    parser.add_argument('-q', '--quiet', action='store_true', help='Print less to stdout')
    return parser.parse_args()


if __name__ == "__main__":
    main()
