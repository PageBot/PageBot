#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#    location.py
#

from copy import copy

class Location(dict):
    """Location object (instead of dictionaries use as location), so we can
    used them as key.

    >>> Location(wght=100, wdth=200)
    <Location wdth=200 wght=100>
    """

    def _get_id(self):
        """Answers a hashable id, that can be used to recreate the Locations instance.

        >>> loc = Location(wght=100, wdth=200)
        >>> loc.id
        (('wdth', 200), ('wght', 100))
        >>> d = {loc.id: loc} # Works as hasable unique id.
        >>> Location.fromId(loc.id) #  Reconstruct location from locId
        <Location wdth=200 wght=100>
        """
        s = []
        for tagValue in sorted(self.items()):
            s += (tagValue,)
        return tuple(s)
    id = property(_get_id)

    def __repr__(self):
        s = '<%s' % self.__class__.__name__

        keys = list(self.keys())
        keys.sort(key=lambda s: s.lower())

        for key in keys:
            v = self.get(key)
            s += ' %s=%s' % (key, v)

        s += '>'
        return s

    def __eq__(self, location):
        return self.id == location.id

    def __ne__(self, location):
        return self.id != location.id

    @classmethod
    def fromId(cls, locId):
        """Convert a locId (tuples) or location dictionary to a Location instance.

        >>> loc = Location.fromId(dict(wght=400, wdth=100))
        >>> loc
        <Location wdth=100 wght=400>
        >>> loc = Location.fromId((('wdth', 100), ('wght', 400)))
        >>> loc
        <Location wdth=100 wght=400>
        """
        location = None
        if isinstance(locId, Location):
            location = copy(locId)
        elif isinstance(locId, dict):
            location = cls()
            for tag, value in locId.items():
                location[tag] = value
        elif isinstance(locId, (tuple, list)):
            location = cls()
            for tag, value in locId:
                location[tag] = value
        return location

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
