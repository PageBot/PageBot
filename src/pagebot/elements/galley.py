# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     galley.py
#
from drawBot import rect

from pagebot.style import NO_COLOR, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot import getFormattedString, setStrokeColor, setFillColor

class Galley(Element):
    u"""A Galley is sticky sequential flow of elements, where the parts can have
    different widths (like headlines, images and tables) or responsive width, such as images
    and formatted text volumes. Size is calculated dynamically, since one of the enclosed
    elements may change width/height at any time during the composition process.
    Also the sequence may change by slicing, adding or removing elements by the Composer.
    Since the Galley is a full compatible Element, it can contain other galley instances
    recursively."""
    from pagebot.elements.textbox import TextBox
    from pagebot.elements.ruler import Ruler
    TEXTBOX_CLASS = TextBox
    RULER_CLASS = Ruler

    def appendString(self, fs):
        u"""Add the string to the laat text box. Create a new textbox if not found."""
        e = self.getLastTextBox()
        if e is None:
            e = self.getTextBox()
        e.appendString(fs)

    def getMinSize(self):
        u"""Cumulation of the maximum minSize of all enclosed elements."""
        minW = minH = 0 # Let's see if we need bigger than this.
        for e in self.elements:
            eMinW, eMinH = e.getMinSize()
            minW = max(minW, eMinW)
            minH += eMinH
        return minW, minH

    def getSize(self):
        u"""Answer the enclosing rectangle of all elements in the galley."""
        w = self.w or 0
        h = self.h or 0
        if w and h: # Galley has fixed/forced size:
            return w, h
        # No fixed size set. Calculate required size from contained elements.
        for e in self.elements:
            ew, eh = e.getSize()
            w = max(w, ew)
            h += eh
        return w, h

    def getWidth(self):
        return self.getSize()[0]

    def getHeight(self):
        return self.getSize()[1]

    def getLastTextBox(self):
        u"""Answer the last text box in the sequence, so we can copy that style."""
        elements = self.elements
        if not elements:
            return None
        for index in range(1, len(elements)-1):
            if elements[-index].isTextBox:
                return elements[-index]
        return None # Not found

    def getLastElement(self):
        u"""Answer the last element in the sequence."""
        elements = self.elements
        if not elements:
            return None
        return elements[-1]

    def getTextBox(self, style=None):
        u"""If the last element is a TextBox, answer it. Otherwise create a new textBox with self.style
        and answer that."""
        lastTextBox = self.getLastTextBox()
        if lastTextBox is not None and style is None:
            style = lastTextBox.style # If not style supplied, copy from the last textBox.
        if lastTextBox is None or lastTextBox != self.getLastElement():
            if style is None: # No last textbox to copy from and no style supplied. Create something here.
                style = dict(w=200, h=0) # Arbitrary width and height, in case not
            self.appendElement(self.TEXTBOX_CLASS('', point=(0, 0), parent=self, style=style))  # Create a new TextBox with style width and empty height.
        return self.getLastElement() # Which only can be a textBox now.

    def newRuler(self, style):
        u"""Add a new Ruler instance, depending on style."""
        ruler = self.RULER_CLASS(style=style)
        self.appendElement(ruler)

    def draw(self, origin, view):
        u"""Like "rolled pasteboard" galleys can draw themselves, if the Composer decides to keep
        them in tact, instead of select, pick & choose elements, until the are all
        part of a page. In that case the w/h must have been set by the Composer to fit the
        containing page."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        setFillColor((1, 1, 0))
        gw, gh = self.getSize()
        rect(px, py, gw, gh)
        gy = 0
        for element in self.elements:
            # @@@ Find space and do more composition
            element.draw((px, py + gy), view)
            gy += element.h

        self._restoreScale()
        view.drawElementMetaInfo(self, origin)

