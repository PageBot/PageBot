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
#     ruler.py
#
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import noColor
from pagebot.toolbox.units import units
from pagebot.constants import DEFAULT_HEIGHT

class Ruler(Element):
    
    def _get_h(self):
        """Poperty for the self.h height value

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> e = Ruler(parent=page, h=3)
        >>> e.h, e.style['h'], e.style['strokeWidth']
        (3pt, 3pt, 3pt)
        >>> e.h = 20
        >>> e.h, e.style['h'], e.style['strokeWidth'] # Identical
        (20pt, 20pt, 20pt)
        >>> e.h = mm(3)
        >>> e.h, e.style['h'], e.style['strokeWidth'] # Identical
        (3mm, 3mm, 3mm)
        """
        base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
        return units(self.css('strokeWidth', 0), base=base)
    def _set_h(self, h): # Overwrite style from here.
        self.style['h'] = self.style['strokeWidth'] = units(h or DEFAULT_HEIGHT) # Overwrite element local style from here, parent css becomes inaccessable.
    h = property(_get_h, _set_h)

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin, **kwargs):
        """Build the Ruler in the current context

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.document import Document
        >>> c = DrawBotContext()
        >>> w, h = pt(300, 400)
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> e = Ruler(parent=page, x=0, y=20, w=page.w, h=3)
        >>> e.build(doc.getView(), pt(0, 0))
        >>> e.xy
        (0pt, 20pt)
        >>> e.size
        (300pt, 3pt)
        >>> view = doc.getView()
        >>> e.build(view, (0, 0))

        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> from pagebot.document import Document
        >>> c = FlatContext()
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> e = Ruler(parent=page, x=0, y=20, w=page.w, h=3)
        >>> # Allow the context to create a new document and page canvas. Normally view does it.
        >>> c.newPage(w, h)
        >>> e.build(doc.getView(), pt(0, 0))
        >>> e.xy
        (0pt, 20pt)
        >>> e.size
        (300pt, 3pt)
        """
        context = self.context # Get current context and builder.
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
        sIndent = self.css('indent')
        sTailIndent = self.css('tailIndent')
        w = self.w - sIndent - sTailIndent

         # Let the view draw frame info for debugging, in case
         # view.showFrame == True
        #view.drawElementFrame(self, p)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        context.fill(noColor)
        context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        context.line((px + sIndent, py), (px + w, py))

        # If there are child elements, recursively draw them over the pixel image.
        self.buildChildElements(view, origin, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin)

    #   H T M L  /  S A S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True, **kwargs):
        """Build the Ruler in the current context

        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> from pagebot.document import Document
        >>> c = HtmlContext()
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> e = Ruler(parent=page, x=0, y=20, w=page.w, h=3)
        >>> e.build(doc.getView(), (0, 0))
        >>> e.xy
        (0pt, 20pt)
        >>> e.size
        (300pt, 3pt)
        >>> view = doc.getView()
        >>> e.build_html(view, (0, 0))
        """

        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context

        context.fill(None)
        context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        #b.line((px + sIndent, py), (px + w, py))

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view)

        b.hr(cssClass=self.cssClass) # Use self.cssClass if defined. Ignore if None.

        if drawElements:
            self.buildChildElements(view, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view)

        self._restoreScale(view)
        #view.drawElementInfo(self, origin)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
