#!/usr/bin/env python

from src.random_selector.models.entrant import Entrant


TEST_ENTRANT_NAME = "tester"


def test_Init_SetInstanceVars_CorrectlySetsInstanceVars():
    expected_entrant_name = TEST_ENTRANT_NAME
    expected_entrant_entries = 1

    actual_entrant = Entrant(expected_entrant_name, expected_entrant_entries)

    assert expected_entrant_name == actual_entrant.name
    assert expected_entrant_entries == actual_entrant.entries


def test_Eq_SetInstanceVars_EntrantsAreEqual():
    first_entrant_name = TEST_ENTRANT_NAME
    first_entrant_entries = 1
    first_entrant = Entrant(first_entrant_name, first_entrant_entries)

    second_entrant_name = TEST_ENTRANT_NAME
    second_entrant_entries = 2
    second_entrant = Entrant(second_entrant_name, second_entrant_entries)

    assert first_entrant == second_entrant