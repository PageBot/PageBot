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
#     color.py
#

import AppKit
from pagebot.errors import PageBotError

# FIXME: solved?
# This should not be here. Make AppKit colors part of DrawBotContext, and for
# the rest use pagebot.toolbox.color functions

class Color:

    colorSpace = AppKit.NSColorSpace.genericRGBColorSpace

    def __init__(self, r=None, g=None, b=None, a=1):
        self._color = None
        if r is None:
            return

        self.r = r
        self.g = g
        self.b = b
        self.a = a

        if isinstance(r, AppKit.NSColor):
            self._color = r
        elif g is None and b is None:
            self._color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(r, r, r, a)
        elif b is None:
            self._color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(r, r, r, g)
        else:
            self._color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)

        self._color = self._color.colorUsingColorSpace_(self.colorSpace())

    def set(self):
        self._color.set()

    def setStroke(self):
        self._color.setStroke()

    def getNSObject(self):
        return self._color

    def copy(self):
        new = self.__class__()
        new._color = self._color.copy()
        return new

    @classmethod
    def getColorsFromList(cls, inputColors):
        outputColors = []
        for color in inputColors:
            color = cls.getColor(color)
            outputColors.append(color)
        return outputColors

    @classmethod
    def getColor(cls, color):
        if isinstance(color, cls.__class__):
            return color
        elif isinstance(color, (tuple, list)):
            return cls(*color)
        elif isinstance(color, AppKit.NSColor):
            return cls(color)
        raise PageBotError("Not a valid color: %s" % color)


class CMYKColor(Color):

    colorSpace = AppKit.NSColorSpace.genericCMYKColorSpace

    def __init__(self, c=None, m=None, y=None, k=None, a=1):
        if c is None:
            return
        if isinstance(c, AppKit.NSColor):
            self._color = c
        else:
            self._color = AppKit.NSColor.colorWithDeviceCyan_magenta_yellow_black_alpha_(c, m, y, k, a)
        self._color = self._color.colorUsingColorSpace_(self.colorSpace())
        self._cmyka = c, m, y, k, a


class Shadow:

    _colorClass = Color

    def __init__(self, offset=None, blur=None, color=None):
        if offset is None:
            return
        self.offset = offset
        self.blur = blur
        self.color = self._colorClass.getColor(color)
        self.cmykColor = None

    def copy(self):
        new = self.__class__()
        new.offset = self.offset
        new.blur = self.blur
        new.color = self.color.copy()
        new.cmykColor = None
        if self.cmykColor:
            new.cmykColor = self.cmykColor.copy()
        return new


class Gradient:

    _colorClass = Color

    def __init__(self, gradientType=None, start=None, end=None, colors=None, positions=None, startRadius=None, endRadius=None):
        if gradientType is None:
            return
        if gradientType not in ("linear", "radial"):
            raise PageBotError("Gradient type must be either 'linear' or 'radial'")
        if not colors or len(colors) < 2:
            raise PageBotError("Gradient needs at least 2 colors")
        if positions is None:
            positions = [i / float(len(colors) - 1) for i in range(len(colors))]
        if len(colors) != len(positions):
            raise PageBotError("Gradient needs a correct position for each color")
        self.gradientType = gradientType
        self.colors = self._colorClass.getColorsFromList(colors)
        self.cmykColors = None
        self.positions = positions
        self.start = start
        self.end = end
        self.startRadius = startRadius
        self.endRadius = endRadius

    def copy(self):
        new = self.__class__()
        new.gradientType = self.gradientType
        new.colors = [color.copy() for color in self.colors]
        new.cmykColors = None
        if self.cmykColors:
            new.cmykColors = [color.copy() for color in self.cmykColors]
        new.positions = list(self.positions)
        new.start = self.start
        new.end = self.end
        new.startRadius = self.startRadius
        new.endRadius = self.endRadius
        return new
