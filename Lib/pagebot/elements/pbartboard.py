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
#     pbartbpoard.py
#
from pagebot.elements.pbgroup import Group

class Artboard(Group):
    """ArtBoard is compatible with the SketchApp element, default identical to Group.

    """

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
