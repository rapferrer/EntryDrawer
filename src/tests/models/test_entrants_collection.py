#!/usr/bin/env python

from src.random_selector.models.entrants_collection import EntrantsCollection
from src.tests.utilities import (
    build_test_entrants_collection,
    build_test_entrant,
    TEST_ENTRANT_NAME,
    TEST_ENTRANT_ENTRIES
)

def test_Init_SetInstanceVars_CorrectlySetsInstanceVars():
    entrants_collection = EntrantsCollection()

    assert entrants_collection.entrants == []
    assert entrants_collection.max_entries == 0
    assert entrants_collection.entrant_entries == {}


def test_AddEntrant_SettingEntrant_EntrantIsAdded():
    first_test_entrant = build_test_entrant()
    expected_entrants = [first_test_entrant]

    entrants_collection = build_test_entrants_collection()

    assert entrants_collection.entrants == expected_entrants
    assert entrants_collection.max_entries == TEST_ENTRANT_ENTRIES
    assert entrants_collection.entrant_entries[TEST_ENTRANT_NAME] == (0, 1)

    second_test_entrant = build_test_entrant("test2", 2)
    expected_entrants.append(second_test_entrant)
    entrants_collection.add_entrant(second_test_entrant)

    assert entrants_collection.entrants == expected_entrants
    assert entrants_collection.max_entries == TEST_ENTRANT_ENTRIES + 2
    assert entrants_collection.entrant_entries["test2"] == (1, 3)


def test_RemoveEntrant_RemovingEntrant_EntrantIsRemoved():
    entrants_collection = build_test_entrants_collection()
    entrants_collection.remove_entrant(TEST_ENTRANT_NAME)

    assert entrants_collection.entrants == []
    assert entrants_collection.max_entries == 0
    assert entrants_collection.entrant_entries == {}


def test_ResetEntries_ResettingEntries_EntriesIsEmpty():
    entrants_collection = build_test_entrants_collection()

    entrants_collection._reset_entries()

    assert entrants_collection.max_entries == 0
    assert entrants_collection.entrant_entries == {}


def test_SetEntries_SetEntrant_EntriesIsUpdated():
    entrants_collection = EntrantsCollection()
    test_entrant = build_test_entrant()

    entrants_collection._set_entries(test_entrant)

    assert entrants_collection.max_entries == TEST_ENTRANT_ENTRIES
    assert entrants_collection.entrant_entries[TEST_ENTRANT_NAME] == (0, 1)


def test_Bool_AddEntrants_ReturnsTrue():
    entrants_collection = build_test_entrants_collection()

    assert entrants_collection


def test_Bool_RemoveEntrants_ReturnsFalse():
    entrants_collection = EntrantsCollection()

    assert not entrants_collection


def test_Contains_AddEntrant_ReturnsTrue():
    test_entrant = build_test_entrant()
    entrants_collection = build_test_entrants_collection([test_entrant])

    assert test_entrant in entrants_collection


def test_Contains_RemoveEntrant_ReturnsFalse():
    test_entrant = build_test_entrant()
    entrants_collection = build_test_entrants_collection([test_entrant])

    entrants_collection.remove_entrant(test_entrant.name)

    assert test_entrant not in entrants_collection
