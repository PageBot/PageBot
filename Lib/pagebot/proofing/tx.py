#!/usr/bin/env python
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

def getScale(size, upem):
    """Vector size to screen size factor."""
    return float(size) / float(upem)

def getAscenderHeight(style, size):
    return style.info.ascender * getScale(size, style.info.unitsPerEm)
