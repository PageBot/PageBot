# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     designspacemodel.py
#
from __future__ import division


class DesignSpaceBase(object):

    def __init__(self, axes):
        assert len(axes) == len(set(a.tag for a in axes)), "Axis tags must be unique"
        self.axes = axes

    def getOutline(self, glyphName, location, penFactory):
        """Create an outline for the requested glyph and location, using
        penFactory to construct a pen. It will be called with a glyphSet argument.
        Return the path/pen, a centerPt and a size as a 3-tuple.
        """
        # XXX it needs to be seen whether the center + size thing actually works.
        # Maybe a rectangle (not necessarily the bounding box) works better.
        raise NotImplementedError()

    def getGlyphName(self, charCode):
        """Return the glyph name associated with charCode (a Unicode code point).
        Should return '.notdef' if the character is not defined."""
        raise NotImplementedError()


class Axis(object):

    def __init__(self, name, minValue, defaultValue, maxValue, tag=None):
        self.name = name
        self.minValue = minValue
        self.defaultValue = defaultValue
        self.maxValue = maxValue
        self.tag = tag or name

    def normalizeValue(self, value):
        # This normalizes the value to be between 0 and 1, so this is not the
        # same as the normalized value in a variable font. This is purely to
        # calculate slider settings.
        return (value - self.minValue) / (self.maxValue - self.minValue)
