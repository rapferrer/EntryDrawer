#!/usr/bin/env python
"""Takes in a list of entrants from a .csv and finds the winner or winners."""

import csv
import json
import logging
import random
from typing import List

from entrant import Entrant
from entrants_collection import EntrantsCollection


JSON = "json"
CSV = "csv"
NEWLINE = chr(10)
NAME_COLUMN = 0
NUMBER_OF_ENTRIES_COLUMN = 1

logger = logging.getLogger(__name__)


def build_entrants(args):
    filename = args.file
    file_type = filename.split(".")[-1]
    
    if file_type == JSON:
        entrants = _build_entrants_with_json(args)
    else:
        entrants = _build_entrants_with_csv(args)

    return entrants


def _build_entrants_with_csv(args):
    """Use the passed in args to build out and return an array of Entrant objects from a .txt
    file."""
    entrants_collection = EntrantsCollection()

    try:
        csv_file = open(str(args.file))
    except IOError as ioe:
        logging.warning(_get_bad_file_name_exception_message(ioe))
    else:
        with csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if (line_count == 0) and not args.no_header:
                    line_count += 1
                else:
                    try:
                        line_count += 1
                        entrant_name = row[NAME_COLUMN].strip()
                        if not _is_unique(entrant_name, entrants_collection):
                            logging.info(f'{entrant_name} has already been added to the list of entrants, but is listed again at row {line_count}. Skipping')
                            continue
                        entries = int(row[NUMBER_OF_ENTRIES_COLUMN], 10)
                        entrant = Entrant(entrant_name, entries)
                        entrants_collection.add_entrant(entrant)
                        if not args.quiet:
                            logging.info(f'{entrant.name} has {entrant.entries} entries')
                            logging.info(f'There is currently a total of {entrants_collection.max_entries} entries')
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

    return entrants_collection


def _build_entrants_with_json(args):
    """Use the passed in args to build out and return an array of Entrant objects from a .json
    file."""
    entrants_collection = EntrantsCollection()

    try:
        jsonFile = open(str(args.file))
    except IOError as ioe:
        logging.warning(_get_bad_file_name_exception_message(ioe))
    else:
        with jsonFile:
            data = json.load(jsonFile)
            for json_entrant in data['entrants']:
                try:
                    name = json_entrant['name']
                    if not _is_unique(name, entrants_collection):
                        continue
                    entries = int(json_entrant['entries'])
                    entrant = Entrant(name, entries)
                    entrants_collection.append(entrant)
                    if not args.quiet:
                        logging.warning(f'{entrant.name} has {entrant.entries} entries')
                        logging.warning(f'There is currently a total of {entrant.max} entries')
                except ValueError as ve:
                    # Catches non-integer characters/sequences
                    logging.warning(f'Oops! Expected an integer (whole number) but didn\'t get one with {name}')
                    logging.warning(f'ValueError: {ve}')
                    continue
    
    return entrants_collection


def _get_bad_file_name_exception_message(io_exception: Exception) -> str:
    return f'Pass in a correct file instead of causing:{NEWLINE}{io_exception}'


def _is_unique(name, entrants_collection: EntrantsCollection):
    """Check to see if a name already belongs to an entrant in the list of entrants."""
    unique = True
    for entrant in entrants_collection.entrants:
        if name == entrant.name:
            logging.info(f'{name} already exists! Skipping')
            unique = False
            break
    return unique


def find_winning_entries(entrants_collection: EntrantsCollection, args) -> List:
    without_removal = args.without_removal

    if without_removal:
        return _find_winning_entries_without_removal(entrants_collection, args.number_of_winners)
    else:
        return _find_winning_entries_with_removal(entrants_collection, args.number_of_winners)


def _find_winning_entry(entrants_collection: EntrantsCollection) -> str:
    """Take in a list of Entrant objects, then find a random entry in the list and selects it as\
    the winner."""
    winning_entry_number = random.randint(0, entrants_collection.max_entries)
    logging.info(f'Time to select a random entry for our winner! Selecting entry number {winning_entry_number}')
    for entrant_name, entrant_entry_range in entrants_collection.entrant_entries.items():
        if entrant_entry_range[0] <= winning_entry_number <= entrant_entry_range[1]:
            return entrant_name


def _find_winning_entries_with_removal(entrants_collection: EntrantsCollection, numberOfWinners):
    """Find x winning entries from the list of entrants(x being the second arg passed in)."""
    winners_list = []
    for _ in range(numberOfWinners):
        winner_name = _find_winning_entry(entrants_collection)
        entrants_collection.remove_entrant(winner_name)
        winners_list.append(winner_name)

    return winners_list


def _find_winning_entries_without_removal(entrants_collection: EntrantsCollection, number_of_winners: int) -> List:
    """Find winners in the entrants list without removing them from the list as they are\
    selected."""
    winners_list = []
    while len(winners_list) < number_of_winners:
        winner_name = _find_winning_entry(entrants_collection)
        if winner_name not in winners_list:
            winners_list.append(winner_name)
        else:
            logging.info(f'Oops. We already selected {winner_name} before! Drawing again!')

    return winners_list
