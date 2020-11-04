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
#    fontinfo.py
#

from pagebot.fonttoolbox.designspace.location import Location

class FontInfo:
    """Holds the design space info for master and instance. """

    def __init__(self, name=None, familyName=None, styleName=None, path=None, location=None, info=None):
        self.name = name or styleName
        self.familyName = familyName or 'Untitled'
        self.styleName = styleName
        self.path = path
        self.location = location
        self.info = info # From the <info> tag.

    def _get_location(self):
        return self._location
    def _set_location(self, location):
        if isinstance(location, (tuple, list, dict)): # Is probably is a locationId, try to convert. Or from dict.
            location = Location.fromId(location)
        assert location is None or isinstance(location, Location), TypeError('"%s" is not of type "%s"' % (location, Location))
        self._location = location
    location = property(_get_location, _set_location)

    def __repr__(self):
        s = '<%s %s-%s' % (self.__class__.__name__, self.familyName, self.styleName or 'NoStyle')
        if self.name and self.styleName != self.name:
            s += '/'+self.name
        s += '>'
        return s

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
