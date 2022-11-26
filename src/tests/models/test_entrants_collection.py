#!/usr/bin/env python

from src.random_selector.models.entrants_collection import EntrantsCollection
from src.tests.utilities import (
    build_test_entrant,
    TEST_ENTRANT_NAME,
    TEST_ENTRANT_ENTRIES
)

def test_Init_SetInstanceVars_CorrectlySetsInstanceVars():
    entrants_collection = EntrantsCollection()

    assert entrants_collection.entrants == []
    assert entrants_collection.max_entries == 0
    assert entrants_collection.entrant_entries == {}


def test_AddEntrant_SettingEntrantObj_EntrantObjIsAdded():
    first_test_entrant = build_test_entrant()
    expected_entrants_list = [first_test_entrant]

    entrants_collection = EntrantsCollection()
    entrants_collection.add_entrant(first_test_entrant)

    assert entrants_collection.entrants == expected_entrants_list
    assert entrants_collection.max_entries == TEST_ENTRANT_ENTRIES
    assert entrants_collection.entrant_entries[TEST_ENTRANT_NAME] == (0, 1)

    second_test_entrant = build_test_entrant("test2", 2)
    expected_entrants_list.append(second_test_entrant)
    entrants_collection.add_entrant(second_test_entrant)

    assert entrants_collection.entrants == expected_entrants_list
    assert entrants_collection.max_entries == TEST_ENTRANT_ENTRIES + 2
    assert entrants_collection.entrant_entries["test2"] == (1, 3)