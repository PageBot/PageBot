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
#     basebeziersegment.py
#

MOVETO = 'moveto'
LINETO = 'lineto'
CURVETO = 'curveto'
CLOSEPATH = 'closepath'
INSTRUCTIONS = (MOVETO, LINETO, CURVETO, CLOSEPATH)

class BaseBezierSegment:
    """Instruction and points that should behave like a segment in a NSPath."""

    def __init__(self, instruction, points):
        """Segment of a Bézier curve."""
        assert instruction in INSTRUCTIONS
        self.instruction = instruction
        self.points = points

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return "<BaseBezierSegment: %s -- %s>" % (self.instruction, str(self.points))
