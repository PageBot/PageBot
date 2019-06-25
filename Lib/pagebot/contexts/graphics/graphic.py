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
#     graphic.py
#
from pagebot.contexts.strings.formattedstring import FormattedString
from pagebot.contexts.color.color import *
from pagebot.contexts.bezierpaths.bezierpath import BezierPath

class Graphic:
    """A graphical object to be drawn."""

    def __init__(self):
        self.colorSpace = Color.colorSpace
        self.blendMode = None
        self.fillColor = Color(0)
        self.strokeColor = None
        self.cmykFillColor = None
        self.cmykStrokeColor = None
        self.shadow = None
        self.gradient = None
        self.strokeWidth = 1
        self.lineDash = None
        self.lineCap = None
        self.lineJoin = None
        self.miterLimit = 10
        self.text = FormattedString()
        self.hyphenation = None
        self.path = None

    def newPath(self):
        self.path = BezierPath()

    def setPath(self, path):
        self.path = path

    def copy(self):
        new = self.__class__()
        new.colorSpace = self.colorSpace
        new.blendMode = self.blendMode
        if self.fillColor is not None:
            new.fillColor = self.fillColor.copy()
        else:
            new.fillColor = None
        if self.strokeColor:
            new.strokeColor = self.strokeColor.copy()
        if self.cmykFillColor:
            new.cmykFillColor = self.cmykFillColor.copy()
        if self.cmykStrokeColor:
            new.cmykStrokeColor = self.cmykStrokeColor.copy()
        if self.shadow:
            new.shadow = self.shadow.copy()
        if self.gradient:
            new.gradient = self.gradient.copy()
        if self.path is not None:
            new.path = self.path.copy()

        new.text = self.text.copy()
        new.hyphenation = self.hyphenation
        new.strokeWidth = self.strokeWidth
        new.lineCap = self.lineCap
        if self.lineDash is not None:
            new.lineDash = list(self.lineDash)
        new.lineJoin = self.lineJoin
        new.miterLimit = self.miterLimit
        return new

    def update(self, context):
        self.updateColorSpace(context)

    # support for color spaces

    def setColorSpace(self, colorSpace):
        self.colorSpace = colorSpace
        self.updateColorSpace(None)

    def updateColorSpace(self, context):
        Color.colorSpace = self.colorSpace
