#!/usr/bin/env python

from typing import List
from src.random_selector.models.entrants_collection import EntrantsCollection
from src.random_selector.models.entrant import Entrant


TEST_ENTRANT_NAME = "test"
TEST_ENTRANT_ENTRIES = 1


def build_test_entrant(name=TEST_ENTRANT_NAME, entries=TEST_ENTRANT_ENTRIES) -> Entrant:
    return Entrant(
        name,
        entries
    )


def build_test_entrants_collection(list_of_entrants: List=[]) -> EntrantsCollection:
    entrants_collection = EntrantsCollection()

    for entrant in list_of_entrants:
        entrants_collection.add_entrant(entrant)

    if not entrants_collection.entrants: entrants_collection.add_entrant(build_test_entrant())

    return entrants_collection