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
#     canvascontext.py
#

from pagebot.contexts.basecontext import BaseContext
from pagebot.contexts.builders.canvasbuilder import CanvasBuilder
from pagebot.canvas.canvas import Canvas

class CanvasContext(BaseContext):

    width = 1000
    height = 800

    def __init__(self):
        super().__init__()
        self.b = CanvasBuilder()
        self.name = self.__class__.__name__
        self.canvas = Canvas((0, 0, -0, -0), delegate=self,
            canvasSize=(self.width, self.height), acceptsMouseMoved=True,
            hasHorizontalScroller=True, hasVerticalScroller=True,
            autohidesScrollers=False, backgroundColor=None,
            drawsBackground=True, flipped=True)

    def getCanvas(self):
        """Canvas group, to be assigned to a Vanilla window or view."""
        return self.canvas

    def draw(self, rect):
        print(rect)
