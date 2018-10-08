#!/usr/bin/env python
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
#     idmlbuilder.py
#
from pagebot.contexts.builders.basebuilder import BaseBuilder
from pagebot.contexts.builders.nonebezierpath import BezierPath
try:
    import simple_idml
except:
    print('Cannot find simple_idml library')

class IDMLBuilder(BaseBuilder):
    """
    >>> b = IDMLBuilder()
    >>> b.newDrawing()
    >>> b.newPage()
    """

    def newPage(self, w=None, h=None):
        pass

    def newDrawing(self, path=None):
        pass

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
