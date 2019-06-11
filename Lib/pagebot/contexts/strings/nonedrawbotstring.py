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
#     nonedrawbotstring.py
#
from pagebot.contexts.strings.babelstring import BabelString
from pagebot.constants import LEFT, DEFAULT_FONT_SIZE, DEFAULT_LANGUAGE
from pagebot.paths import DEFAULT_FONT_PATH
from pagebot.toolbox.units import pt

class NoneDrawBotString(BabelString):
    """Used for testing DrawBotString doctest in non-DrawBot Environment."""
    BABEL_STRING_TYPE = 'fs'

    def __init__(self, s, context, style=None):
        self.context = context
        self.s = s
        self.fontSize = DEFAULT_FONT_SIZE
        self.font = DEFAULT_FONT_PATH
        assert style is None or isinstance(style, dict)
        self.style = style
        self.language = DEFAULT_LANGUAGE
        self.hyphenation = False

        self.fittingFont = None # In case we are sampling with a Variable Font.
        self.fittingLocation = None
        self.isFitting = False

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None,
            pixelFit=True, fontSize=None, font=None, tagName=None):
        assert style is None or isinstance(style, dict)
        return cls(s, context=context, style=style)

    def textSize(self, w=None, h=None):
        """Answers the (w, h) size for a given width, with the current text,
        measured from bottom em-size to top-emsize (including ascender+ and
        descender+) and the string width (including margins)."""
        return w or 100, h or 100

    def __repr__(self):
        return self.s

    def fill(self, r, g=None, b=None, a=None, alpha=None):
        pass

    setFillColor = fill

    def cmykFill(self, c, m=None, y=None, k=None, a=None, alpha=None):
        pass

    cmykStroke = cmykFill

    def stroke(self, r, g=None, b=None, a=None, alpha=None):
        pass

    setStrokeColor = stroke

    def setStrokeWidth(self, w):
        pass

    strokeWidth = setStrokeWidth

    def getTextLines(self, w, h=None, align=LEFT):
        return {}

    def _get_size(self):
        return pt(0, 0)
    size = property(_get_size)
