#!/usr/bin/env python
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
#     gradient.py
#

class Gradient(object):
    u"""
    As linear gradient (startRadius or endRadius not set):
    startPoint as (x, y)
    endPoint as (x, y)
    colors as a list of colors, described similary as fill
    locations of each color as a list of floats. (optionally)
    Setting a gradient will ignore the fill.

    As radial gradiens (startRadius and endRadius are set):
    startPoint as (x, y)
    endPoint as (x, y)
    colors as a list of colors, described similary as fill
    locations of each color as a list of floats. (optionally)
    startRadius radius around the startPoint in degrees (optionally)
    endRadius radius around the endPoint in degrees (optionally)
    Setting a gradient will ignore the fill.
    """
    def __init__(self, start=None, end=None, colors=None, cmykColors=None, locations=None,
        startRadius=None, endRadius=None):
        # TODO: Add assert test of locations has same length as colors.
        self.start = start or (0.5, 0) # Default to start a center of bottom.
        self.end = end or (0.5, 1) # Default to end at center of top.
        self.colors = colors or ((0,0,0), (1,1,1)) # Default to run between black and white.
        self.cmykColors = None
        self.locations = locations or [0,1]
        self.startRadius = startRadius
        self.endRadius = endRadius
        # Make sure that lengths of colors and locations are identical.
        assert len(self.colors) == len(self.locations)

    def _get_linear(self):
        return not self.radial
    linear = property(_get_linear)

    def _get_radial(self):
        return self.startRadius is not None and self.endRadius is not None
    radial = property(_get_radial)

class Shadow(object):
    def __init__(self, offset=None, blur=None, color=None, cmykColor=None):
        self.offset = offset or (5, -5)
        self.blur = blur
        self.color = color
        self.cmykColor = cmykColor


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
