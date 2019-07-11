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
#     pattern.py
#

class FoundPattern:

    def __init__(self, s, x, ix, y=None, w=None, h=None, line=None, run=None):
        self.s = s # Actual found string
        self.x = x
        self.ix = ix
        self.y = y
        self.w = w
        self.h = h
        self.line = line # TextLine instance that this was found in
        self.run = run # List of  of this strin,g

    def __repr__(self):
        return '[Found "%s" @ %d,%d]' % (self.s, self.x, self.y)

    #   F I N D

def findPattern(textLines, pattern):
    """Answers the point locations where this pattern occures in the Formatted
    String."""
    foundPatterns = [] # List of FoundPattern instances.
    for lineIndex, textLine in enumerate(textLines):
        for foundPattern in textLine.findPattern(pattern):
            foundPattern.y = textLine.y
            foundPattern.z = 0
            foundPatterns.append(foundPattern)
    return foundPatterns


