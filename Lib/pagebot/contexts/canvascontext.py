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

class CanvasContext(BaseContext):

    def __init__(self):
        super().__init__()
        self.b = CanvasBuilder()
        self.name = self.__class__.__name__

    def newPage(self, width, height):
        return self.b.newPage(width, height)


