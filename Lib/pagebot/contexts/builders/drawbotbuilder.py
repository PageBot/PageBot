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
#     drawbotbuilder.py
#

try:
    import drawBot
    drawBotBuilder = drawBot
    # Id to make builder hook name. Views will be calling e.build_html()
    drawBotBuilder.PB_ID = 'drawBot' 
    # Text by import if MacOS specific imports are available.
    import CoreText, AppKit, Quartz # #pylint: disable=unused-import

except ImportError:
    drawBotBuilder = None

class NoneDrawBotBuilder(object):
    """Make NoneDrawBotBuilder with the same API for docTesting, in case the platform does not support DrawBot.
    More methods to be added here, if DrawBotContext docTests fail in non-DrawBot platforms.
    Eventually should be a matching set of methods, compare to DrawBot itself."""

    PB_ID = 'drawBot'

    def newDrawing(self):
        pass

    restore = save = newPath = drawPath = newDrawing # Nethods without attributes

    def scale(self, sx, sy):
        pass

    def translate(self, x, y):
        pass

    def newPage(self, w, h):
        pass

    def moveTo(self, p):
        pass

    lineTo = moveTo

    def openTypeFeatures(self, **openTypeFeatures):
        pass

    def oval(self, x, y, w, h):
        pass

    rect = oval

    def fill(self, c):
        pass

    setFillColor = fill

    def stroke(self, c, w=1):
        pass

    setStrokeColor = stroke

    def sizes(self):
        return dict(screen=(800, 600))

    def fontSize(self, fontSize):
        pass

    def FormattedString(self, s):
        return s


noneDrawBotBuilder = NoneDrawBotBuilder()
