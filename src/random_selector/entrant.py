#!/usr/bin/env python


class Entrant:
    """Object represents an individual in a competition with a number of entries."""

    def __init__(self, min, max, entries, name):
        """Define the Entrant class."""
        self.min = min
        self.max = max
        self.entries = entries
        self.name = name