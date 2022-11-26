#!/usr/bin/env python

from src.random_selector.models.entrant import Entrant
from .models.test_entrant import TEST_ENTRANT_NAME


TEST_ENTRANT_NAME = "test"
TEST_ENTRANT_ENTRIES = 1


def build_test_entrant(name=TEST_ENTRANT_NAME, entries=TEST_ENTRANT_ENTRIES) -> Entrant:
    return Entrant(
        name,
        entries
    )