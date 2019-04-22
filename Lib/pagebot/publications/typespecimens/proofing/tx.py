#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------

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
#     tx.py
#

def getScale(font, size):
    """Vector size to screen size factor."""
    return float(size) / float(font.info.unitsPerEm)

def getAscenderHeight(font, size):
    return font.info.ascender * getScale(font, size)
