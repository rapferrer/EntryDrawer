#!/usr/bin/env python


class Entrant:
    """Object represents an individual in a competition with a number of entries."""

    def __init__(self, name: str, entries: int):
        self.entries = entries
        self.name = name


    def __eq__(self, other_name):
        """Return True if the given name matches this entrants name"""
        return self.name == other_name