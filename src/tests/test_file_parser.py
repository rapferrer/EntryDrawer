#!/usr/bin/env python

from src.random_selector.file_parser import (
    _parse_entrant_from_dict,
    _parse_entrant_from_list,
    NAME_COLUMN,
    NUMBER_OF_ENTRIES_COLUMN
)
# def _parse_entrant_from_json(json_entrant: Dict) -> Entrant:
#     return Entrant(
#         json_entrant['name'],
#         json_entrant['entries']
#     )


def test_ParseEntrantFromJson_SetJsonEntrant_ReturnsEntrant():
    entrant_dict = {
        "name": "test",
        "entries": 1
    }

    entrant = _parse_entrant_from_dict(entrant_dict)

    assert entrant.name == entrant_dict["name"]
    assert entrant.entries == entrant_dict["entries"]


def test_ParseEntrantFromList_SetList_ReturnsEntrant():
    entrant_list = [
        "test",
        "1"
    ]

    entrant = _parse_entrant_from_list(entrant_list)

    assert entrant.name == entrant_list[NAME_COLUMN]
    assert entrant.entries == int(entrant_list[NUMBER_OF_ENTRIES_COLUMN], 10)