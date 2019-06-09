#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     gradient.py
#
from pagebot.toolbox.color import blackColor, whiteColor, color as makeColor
from pagebot.toolbox.units import units

class Gradient:
    """As linear gradient (startRadius or endRadius not set):

    startPoint as (x, y)
    endPoint as (x, y)

    colors as a list of Colors instances, described similary as fill locations
    of each Color as a list of floats. (optionally) Setting a gradient will
    ignore the fill.

    As radial gradient (startRadius and endRadius are set):

    startPoint as (x, y)
    endPoint as (x, y)

    colors as a list of Colors instances, described similary as fill
    locations of each color as a list of floats. (optionally)
    startRadius radius around the startPoint in degrees (optionally)
    endRadius radius around the endPoint in degrees (optionally)
    Setting a gradient will ignore the fill.
    """
    def __init__(self, start=None, end=None, colors=None, locations=None,
            startRadius=None, endRadius=None):
        #assert color is None or isinstance(color, Color)
        self.start = start or (0.5, 0) # Default to start at center of bottom.
        self.end = end or (0.5, 1) # Default to end at center of top.
        self.colors = colors or (blackColor, whiteColor) # Default to run between black and white.
        self.locations = locations or [0, 1]
        self.startRadius = startRadius
        self.endRadius = endRadius
        # Make sure that lengths of colors and locations are identical.
        assert len(self.colors) == len(self.locations) == len(self.start) == len(self.end)

    def _get_linear(self):
        return not self.radial
    linear = property(_get_linear)

    def _get_radial(self):
        """Answers the radial type flag, as result of there is a radius defined."""
        return self.startRadius is not None and self.endRadius is not None
    radial = property(_get_radial)

class Shadow:

    def __init__(self, offset=None, blur=None, color=None):
        """Set he parameter of the Shadow instance.
        TODO: Make optional to use the z-position of an element really cast the shadow,
        defining both the offset (from light-source position) and blur from distance.

        >>> shadow = Shadow()
        >>> shadow
        <Shadow offset=(6pt, -6pt) blur=6pt Color(r=0, g=0, b=0)>
        """
        self.offset = units(offset or (6, -6))
        if blur is None: # In case not defined, attach to offset.
            blur = self.offset[0]
        self.blur = units(blur)
        if color is None:
            self.color = blackColor
        else:
            self.color = makeColor(color)

    def __repr__(self):
        return '<%s offset=%s blur=%s %s>' % (self.__class__.__name__, self.offset, self.blur, self.color)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
