#!/usr/bin/env python
"""Takes in a list of entrants from a .csv and finds the winner or winners."""

from argparse import Namespace
import csv
import json
import logging

from typing import Dict, List

from src.random_selector.models.entrant import Entrant
from src.random_selector.models.entrants_collection import EntrantsCollection


JSON = "json"
CSV = "csv"
NAME_COLUMN = 0
NUMBER_OF_ENTRIES_COLUMN = 1

logger = logging.getLogger(__name__)


def build_entrants(args: Namespace) -> EntrantsCollection:
    filename = args.file
    file_type = filename.split(".")[-1]
    entrants_collection = EntrantsCollection()
    
    if file_type == JSON:
        entrants_collection = _build_entrants_with_json_file(args)
    elif file_type == CSV:
        entrants_collection = _build_entrants_with_csv_file(args)
    else:
        logger.info(f'Unsupported file type: {file_type}')

    return entrants_collection


def _build_entrants_with_csv_file(args: Namespace) -> EntrantsCollection:
    """Use the passed in args to build out and return an array of Entrant objects from a .csv
    file."""
    entrants_collection = EntrantsCollection()

    with open(str(args.file), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        entrants_collection = _parse_entrants_from_csv_rows(csv_reader, args.quiet, args.no_header)

    return entrants_collection


def _parse_entrants_from_csv_rows(csv_reader, quiet_output: bool, no_header: bool) -> EntrantsCollection:
    entrants_collection = EntrantsCollection()
    row_number = 0

    for row in csv_reader:
        if (row_number == 0) and not no_header:
            row_number += 1
            continue
        else:
            try:
                entrant = _parse_entrant_from_list(row)
                if entrant not in entrants_collection:
                    entrants_collection.add_entrant(entrant)
                    if not quiet_output:
                        _log_entrant(entrant, entrants_collection)
                else:
                    logger.info(f'{entrant.name} already exists! Skipping')

                row_number += 1
            except ValueError as ve:
                _handle_value_error(ve, row)
                continue
            except IndexError as ie:
                # Catches emtpy lines
                logger.warning(f'Oops! Expected info on line {row_number + 1} but found nothing!')
                logger.warning(f'IndexError: {ie}')
                continue

    return entrants_collection


def _parse_entrant_from_list(row: List) -> Entrant:
    return Entrant(
        row[NAME_COLUMN].strip(),
        int(row[NUMBER_OF_ENTRIES_COLUMN], 10)
    )  


def _build_entrants_with_json_file(args: Namespace) -> EntrantsCollection:
    """Use the passed in args to build out and return an array of Entrant objects from a .json
    file."""
    entrants_collection = EntrantsCollection()

    with open(str(args.file)) as json_file:
        data = json.load(json_file)
        entrants_collection = _parse_entrants_from_dict(data, args.quiet)

    return entrants_collection


def _parse_entrants_from_dict(data: Dict, quiet_output: bool) -> EntrantsCollection:
    entrants_collection = EntrantsCollection()

    for entrant_obj in data['entrants']:
        try:
            entrant = _parse_entrant_from_dict(entrant_obj)
            if entrant not in entrants_collection:
                entrants_collection.add_entrant(entrant)
                if not quiet_output:
                    _log_entrant(entrant, entrants_collection)
            else:
                logger.info(f'{entrant.name} already exists! Skipping')

        except ValueError as ve:
            _handle_value_error(ve, entrant_obj)
            continue

    return entrants_collection


def _parse_entrant_from_dict(entrant: Dict) -> Entrant:
    return Entrant(
        entrant['name'],
        entrant['entries']
    )


def _log_entrant(entrant: Entrant, entrants_collection: EntrantsCollection):
    logger.info(f'{entrant.name} has {entrant.entries} entries')
    logger.info(f'There is currently a total of {entrants_collection.max_entries} entries') 


def _handle_value_error(value_error: ValueError, unparsed_obj):
    message_prefix = f'Oops! Expected an integer (whole number) but didn\'t get one with '
    if isinstance(unparsed_obj, List):
        message_suffix = f'row {unparsed_obj}'
    elif isinstance(unparsed_obj, Dict):
        message_suffix = f'{unparsed_obj}'
    else:
        raise TypeError(f'Unrecognized object passed to value error handler: {unparsed_obj}')

    logger.warning(message_prefix + message_suffix)
    logger.warning(f'ValueError: {value_error}') 