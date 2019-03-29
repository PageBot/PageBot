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
#     galley.py
#
from pagebot.constants import ORIGIN
from pagebot.elements.element import Element
from pagebot.elements.pbtextbox import TextBox
from pagebot.elements.pbruler import Ruler
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import color
from pagebot.conditions import *

class Galley(Element):
    """A Galley is a sticky sequential flow of elements, where the parts can
    have different widths (like headlines, images and tables) or responsive
    width, such as images and formatted text volumes. Size is calculated
    dynamically, since one of the enclosed elements may change width/height at
    any time during the composition process. Also the sequence may change by
    slicing, adding or removing elements by the Composer. Because the Galley is
    a fully compatible Element, it can contain other galley instances
    recursively."""

    TEXTBOX_CLASS = TextBox
    RULER_CLASS = Ruler
    OLD_PAPER_COLOR = color(rgb=0xF8ECC2) # Color of old paper: #F8ECC2

    def __init__(self, fill=None, conditions=None, **kwargs):
        Element.__init__(self,  **kwargs)
        # Make sure that this is a formatted string. Otherwise create it with
        # the current style.

        if fill is None: # Set default Galley color if not defined.
            fill = self.OLD_PAPER_COLOR
        self.fill = fill

        if conditions is None:
            conditions = [Fit(), Overflow2Next()]
        self.conditions = conditions

        e = self.TEXTBOX_CLASS(conditions=[Fit()]) # First textbox on the Galley
        self.appendElement(e) # Attach it to the galley self.

    def append(self, bs):
        """Add the string to the last text box. Create a new textbox if not found."""
        if self.lastTextBox is None:
            self.newTextBox(bs) # Also sets self.lastTextBox
        else:
            self.lastTextBox.append(bs)

    def appendElement(self, e):
        """Add element to the list of child elements. Note that elements can be
        added multiple times.  If the element is alread placed in another
        container, then remove it from its current parent.  This relation and
        position is lost. The position e is supposed to be filled already in
        local position."""
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
        """Answers the enclosing rectangle of all elements in the galley."""
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
        """Answers the last element in the sequence."""
        elements = self.elements
        if not elements:
            return None
        return elements[-1]

    def newTextBox(self, bs):
        """Create a new *self.TEXTBOX_CLASS* instance, filled with the *fs*
        BabelString. The actual type of string depends on the current content. 
        Append the element to *self* (also setting self.lastTextBox) and answer the element."""
        tb = self.TEXTBOX_CLASS(bs, parent=self)
        self.appendElement(tb) # Will set the self.lastTextBox by local self.appendElement(tb)
        return tb

    def newRuler(self, style):
        """Add a new Ruler instance, depending on style."""
        ruler = self.RULER_CLASS(style=style)
        self.appendElement(ruler)

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True, **kwargs):
        """Like "rolled pasteboard" galleys can draw themselves, if the
        Composer decides to keep them in tact, instead of select, pick & choose
        elements, until the are all part of a page. In that case the w/h must
        have been set by the Composer to fit the containing page."""
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.

        # Let the view draw frame info for debugging, in case
        # view.showFrame == True
        view.drawElementFrame(self, p)

        if self.drawBefore is not None:
            self.drawBefore(self, view, p)

        self.context.fill(self.css('fill')) # Find old-paper background color
        gw, gh = self.getSize()
        self.context.rect(px, py, gw, gh)

        if drawElements:
            hook = 'build_' + self.context.b.PB_ID
            # Don't call self.buildElements, we want to track the vertical
            # positions.
            gy = 0
            for e in self.elements:
                if not e.show:
                    continue
                # @@@ Find space and do more composition
                if hasattr(e, hook):
                    getattr(e, hook)(view, (px, py + gy), **kwargs)
                else:
                    # No implementation for this context, call default building
                    # method for this element.
                    e.build(view, (px, py + gy), **kwargs)
                gy += e.h

        if self.drawAfter is not None:
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin)

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, path, drawElements=True, **kwargs):
        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view)

        if drawElements:
            self.buildElements(self, view, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view)

class Column(Galley):
    """A Column is very similar to a Galley, grouping elements together in sequential order.
    The reason for creating a separate class is that Galley is focused on the input
    (as generated by a Typesetter), where a Column instance is oriented on output, layout
    on a pages, etc.
    """

    def build_html(self, view, path, drawElements=True, **kwargs):

        context = view.context # Get current context.
        b = context.b

        # Use self.cssClass if defined, otherwise self class. #id is ignored if None
        b.div(cssClass=self.cssClass or self.__class__.__name__.lower(), cssId=self.cssId)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view)

        if drawElements:
            for e in self.elements:
                e.build_html(view, path, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view)

        b._div() # self.cssClass or self.__class__.__name__

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
