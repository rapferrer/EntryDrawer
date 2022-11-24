#!/usr/bin/env python
"""Takes in a list of entrants from a .csv and finds the winner or winners."""

import csv
import json
import logging
import random

from entrant import Entrant


JSON = "json"
CSV = "csv"
NEWLINE = chr(10)

logger = logging.getLogger(__name__)


def buildEntrants(args):
    filename = args.file
    file_type = filename.split(".")[-1]
    
    if file_type == JSON:
        entrants = _buildEntrantsJson(args)
    else:
        entrants = _buildEntrantsTxt(args)

    return entrants


def _buildEntrantsTxt(args):
    """Use the passed in args to build out and return an array of Entrant objects from a .txt
    file."""
    entrants = []
    try:
        csv_file = open(str(args.file))
    except IOError as ioe:
        logging.warning(_get_bad_file_name_exception_message(ioe))
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
                        if not _isUnique(strippedName, entrants):
                            continue
                        entries = int(row[1], 10)
                        entrant = Entrant(minimum, minimum + entries, entries, strippedName)
                        minimum = minimum + entries
                    except ValueError as ve:
                        # Catches non-integer characters/sequences
                        logging.warning(f'Oops! Expected an integer (whole number) but didn\'t get one "\
                              "after {row[0]} in row {line_count}')
                        logging.warning(f'ValueError: {ve}')
                        continue
                    except IndexError as ie:
                        # Catches emtpy lines
                        logging.warning(f'Oops! Expected info on line {line_count} but found nothing!')
                        logging.warning(f'IndexError: {ie}')
                        continue
                    entrants.append(entrant)
                    if not args.quiet:
                        logging.info(f'{entrant.name} has {entrant.entries} entries')
                        logging.info(f'There is currently a total of {entrant.max} entries')
    
    return entrants


def _buildEntrantsJson(args=None):
    """Use the passed in args to build out and return an array of Entrant objects from a .json
    file."""
    entrants = []
    try:
        jsonFile = open(str(args.file))
    except IOError as ioe:
        logging.warning(_get_bad_file_name_exception_message(ioe))
    else:
        with jsonFile:
            minimum = 0
            data = json.load(jsonFile)
            for jsonObject in data['entrants']:
                # Create the entrant object
                try:
                    name = jsonObject['name']
                    if not _isUnique(name, entrants):
                        continue
                    entries = int(jsonObject['entries'])
                    entrant = Entrant(minimum, minimum + entries, entries, name)
                    minimum = minimum + entries
                except ValueError as ve:
                    # Catches non-integer characters/sequences
                    logging.warning(f'Oops! Expected an integer (whole number) but didn\'t get one with {name}')
                    logging.warning(f'ValueError: {ve}')
                    continue
                entrants.append(entrant)
                if not args.quiet:
                    logging.warning(f'{entrant.name} has {entrant.entries} entries')
                    logging.warning(f'There is currently a total of {entrant.max} entries')
    
    return entrants


def _get_bad_file_name_exception_message(io_exception: Exception) -> str:
    return f'Pass in a correct file instead of causing:{NEWLINE}{io_exception}'


def _isUnique(name, entrants):
    """Check to see if a name already belongs to an entrant in the list of entrants."""
    unique = True
    for existingEntrant in entrants:
        if name == existingEntrant.name:
            logging.info(f'{name} already exists! Skipping')
            unique = False
            break
    return unique


def findWinningEntries(entrants, args):
    without_removal = args.without_removal

    if without_removal:
        return _findWinningEntriesWithoutRemoval(entrants, args.number_of_winners)
    else:
        return _findWinningEntriesWithRemoval(entrants, args.number_of_winners)


def _findWinningEntry(entrants, withRemoval):
    """Take in a list of Entrant objects, then find a random entry in the list and selects it as\
    the winner."""
    logging.info(f'Time to select a random entry for our winner!')
    winningEntry = entrants[-1].max % random.randint(0, entrants[-1].max)
    logging.info(f'Selecting entry number {winningEntry}')
    for entrant in entrants:
        if winningEntry < entrant.max:
            if withRemoval:
                logging.info(f'Our winner is {entrant.name}')
            return entrant


def _findWinningEntriesWithRemoval(entrants, numberOfWinners):
    """Find x winning entries from the list of entrants(x being the second arg passed in)."""
    winner = _findWinningEntry(entrants, True)
    if (numberOfWinners > 1):
        reducedEntrants = _removeWinner(entrants, winner)
        _findWinningEntriesWithRemoval(reducedEntrants, numberOfWinners - 1)
    return winner


def _removeWinner(entrants, winner):
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


def _findWinningEntriesWithoutRemoval(entrants, numberOfWinners):
    """Find winners in the entrants list without removing them from the list as they are\
    selected."""
    winnerEntrants = []
    x = 0
    while x < numberOfWinners:
        winner = _findWinningEntry(entrants, False)
        if winner not in winnerEntrants:
            winnerEntrants.append(winner)
            x += 1
        else:
            logging.info(f'Oops. We selected " + winner.name + " a second time! Drawing again!')
    _printWinners(winnerEntrants)
    return


def _printWinners(winners):
    """Print a list of Entrant objects."""
    logging.info(f'Here are our winners!')
    for winner in winners:
        logging.info(winner.name)
    return
