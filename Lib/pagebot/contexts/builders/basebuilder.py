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
#     basebuilder.py
#

import os
from pagebot.toolbox.transformer import path2Name

class BaseBuilder:
    """The BaseBuilder is the abstract builder class, for all builders that
    need to import and write files in a directory, or draw on their builders,
    besides the binary export formats that are already supported by e.g.
    DrawBot."""

    def __init__(self):
        self._installedFonts = []

    def installedFonts(self, pattern=None):
        return []

    #   T E X T

    def installFont(self, fontPath):
        self._installedFonts.append(fontPath)
        if os.path.exists(fontPath):
            return path2Name(fontPath)
        return None

    def fontName2FontPath(self, fontName):
        """We cannot tell the relation of the font name and the font path for
        DrawBot without OS X unless it is a path."""
        if os.path.exists(fontName):
            return fontName
        return None

    def FormattedString(self, s):
        class FS:
            def __init__(self, s):
                self.s = s
        return FS(s)

    def frameDuration(self, frameDuration):
        pass

    def save(self):
        pass

