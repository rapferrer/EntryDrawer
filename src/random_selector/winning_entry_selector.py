#!/usr/bin/env python
"""Takes in a list of entrants from a .csv and finds the winner or winners."""


from argparse import Namespace
import logging
import random
from typing import List

from models.entrants_collection import EntrantsCollection


logger = logging.getLogger(__name__)


def find_winning_entries(entrants_collection: EntrantsCollection, args: Namespace) -> List:
    without_removal = args.without_removal

    if without_removal:
        return _find_winning_entries_without_removal(entrants_collection, args.number_of_winners)
    else:
        return _find_winning_entries_with_removal(entrants_collection, args.number_of_winners)


def _find_winning_entry(entrants_collection: EntrantsCollection) -> str:
    """Take in a list of Entrant objects, then find a random entry in the list and selects it as\
    the winner."""
    winning_entrant = ""
    winning_entry_number = random.randint(0, entrants_collection.max_entries)
    logger.info(f'Time to select a random entry for our winner! Selecting entry number {winning_entry_number}')
    for entrant_name, entrant_entry_range in entrants_collection.entrant_entries.items():
        if entrant_entry_range[0] < winning_entry_number <= entrant_entry_range[1]:
            winning_entrant = entrant_name
            break

    return winning_entrant


def _find_winning_entries_with_removal(entrants_collection: EntrantsCollection, numberOfWinners: int) -> List:
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
            logger.info(f'Oops. We already selected {winner_name} before! Drawing again!')

    return winners_list
