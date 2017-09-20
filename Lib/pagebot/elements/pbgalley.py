# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#     
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     galley.py
#
from pagebot.style import NO_COLOR, ORIGIN, makeStyle
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset, int2Color

class Galley(Element):
    u"""A Galley is sticky sequential flow of elements, where the parts can have
    different widths (like headlines, images and tables) or responsive width, such as images
    and formatted text volumes. Size is calculated dynamically, since one of the enclosed
    elements may change width/height at any time during the composition process.
    Also the sequence may change by slicing, adding or removing elements by the Composer.
    Since the Galley is a full compatible Element, it can contain other galley instances
    recursively."""
    from pagebot.elements.pbtextbox import TextBox
    from pagebot.elements.pbruler import Ruler
    TEXTBOX_CLASS = TextBox
    RULER_CLASS = Ruler
        
    OLD_PAPER_COLOR = int2Color(0xF8ECC2) # Color of old paper: #F8ECC2

    def __init__(self, **kwargs):
        Element.__init__(self,  **kwargs)
        # Make sure that this is a formatted string. Otherwise create it with the current style.
        # Note that in case there is potential clash in the double usage of fill and stroke.
        self.lastTextBox = None

    def appendString(self, fs):
        u"""Add the string to the laat text box. Create a new textbox if not found."""
        if self.lastTextBox is None:
            self.newTextBox(fs) # Also sets self.lastTextBox 
        else:
            self.lastTextBox.appendString(fs)

    def appendHtml(self, html):
        u"""Add the utf-8 html to the laat text box. Create a new textbox if not found."""
        if self.lastTextBox is None:
            self.newTextBox('', html=html) # Also sets self.lastTextBox 
        else:
            self.lastTextBox.appendHtml(html)

    def getMinSize(self):
        u"""Cumulation of the maximum minSize of all enclosed elements."""
        minW = minH = 0 # Let's see if we need bigger than this.
        for e in self.elements:
            eMinW, eMinH = e.getMinSize()
            minW = max(minW, eMinW)
            minH += eMinH
        return minW, minH

    def appendElement(self, e):
        u"""Add element to the list of child elements. Note that elements can be added multiple times.
        If the element is alread placed in another container, then remove it from its current parent.
        This relation and position is lost. The position e is supposed to be filled already in local position."""
        eParent = e.parent
        if not eParent is None: 
            eParent.removeElement(e) # Remove from current parent, if there is one.
        self._elements.append(e) # Possibly add to self again, will move it to the top of the element stack.
        e.setParent(self) # Set parent of element without calling this method again.
        if e.eId: # Store the element by unique element id, if it is defined.
            self._eIds[e.eId] = e
        # If this is a text box, then set self.lastTextBox
        if e.isTextBox:
            self.lastTextBox = e
        return len(self._elements)-1 # Answer the element index for e.

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

    def getLastElement(self):
        u"""Answer the last element in the sequence."""
        elements = self.elements
        if not elements:
            return None
        return elements[-1]

    def newTextBox(self, fs, html=None):
        u"""Create a new *self.TEXTBOX_CLASS* instance, filled with the *fs* FormattedString.
        Append the element to *self* (also setting self.lastTextBox) and answer the element."""
        tb = self.TEXTBOX_CLASS('', parent=self, html=html)
        self.appendElement(tb) # Will set the self.lastTextBox by local self.appendElement(tb)
        return tb

    def newRuler(self, style):
        u"""Add a new Ruler instance, depending on style."""
        ruler = self.RULER_CLASS(style=style)
        self.appendElement(ruler)

    #   D R A W B O T  S U P P O R T

    def build_drawBot(self, view, origin=ORIGIN, drawElements=True):
        u"""Like "rolled pasteboard" galleys can draw themselves, if the Composer decides to keep
        them in tact, instead of select, pick & choose elements, until the are all
        part of a page. In that case the w/h must have been set by the Composer to fit the
        containing page."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(view, p)

        view.setFillColor(self.OLD_PAPER_COLOR) # Color of old paper: #F8ECC2
        gw, gh = self.getSize()
        b.rect(px, py, gw, gh)
        if drawElements:
            gy = 0
            for e in self.elements:
                # @@@ Find space and do more composition
                e.build_drawBot(view, (px, py + gy))
                gy += element.h

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)

    #   F L A T  S U P P O R T

    def build_flat(self, view, origin=ORIGIN, drawElements=True):
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(view, p)

        if drawElements:
            for e in self.elements:
                e.build_flat(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(view, p)
        
    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, origin, view, drawElements=True):

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(view, p)

        if drawElements:
            for e in self.elements:
                e.build_html(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(view, p)


