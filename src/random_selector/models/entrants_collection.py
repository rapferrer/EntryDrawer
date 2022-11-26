#!/usr/bin/env python


from entrant import Entrant


class EntrantsCollection:
    """A collection of Entrant objects."""
    
    def __init__(self):
        self.entrants = []
        self._reset_entries()

    
    def add_entrant(self, entrant: Entrant):
        self.entrants.append(entrant)
        self._set_entries(entrant)


    def remove_entrant(self, entrant_name: str):
        self.entrants.remove(entrant_name)
        self._reset_entries()
        for entrant in self.entrants:
            self._set_entries(entrant)


    def _reset_entries(self):
        self.max_entries = 0
        self.entrant_entries = {}


    def _set_entries(self, entrant: Entrant):
        new_max_entries = self.max_entries + entrant.entries
        self.entrant_entries[entrant.name] = (self.max_entries, new_max_entries)
        self.max_entries = new_max_entries


    def __bool__(self):
        """Return True if any Entrant objects have been added to the collection. Otherwise return False."""
        if self.entrants:
            return True
        else:
            return False

    
    def __contains__(self, entrant: Entrant):
        """Returns True if the given Entrant object is already a part of the entrants list"""
        for existing_entrant in self.entrants:
            if entrant.name == existing_entrant.name:
                return True
        
        return False
