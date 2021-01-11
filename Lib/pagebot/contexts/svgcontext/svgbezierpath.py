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
#     svgbezierpath.py
#

'''
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.pens.boundsPen import BoundsPen
from pagebot.errors import PageBotError
from pagebot.constants import MOVETO, LINETO, CURVETO, CLOSEPATH
'''
from pagebot.contexts.basecontext.basebezierpath import BaseBezierPath


class SvgBezierPath(BaseBezierPath):
    """Bézier path that implements commands like SVG, but with the same API
    as DrawBot.BezierPath, based on the FontTools pen implementation.
    """

    def __init__(self, b, path=None, glyphSet=None):
        self.b = b
        self.commands = []
        super().__init__(path=path, glyphSet=glyphSet)

    def __repr__(self):
        return '<SvgBezierPath>'
