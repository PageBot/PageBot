#!/usr/bin/env python
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
#     ruler.py
#
from pagebot.elements.element import Element
from pagebot.toolbox.transformer import pointOffset
from pagebot.style import NO_COLOR

class Ruler(Element):

    def _get_h(self):
        u"""Poperty for the self.h height value 

        >>> from pagebot.document import Document
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30)
        >>> page = doc[1]
        >>> e = Ruler(parent=page, h=3)
        >>> e.h, e.style['h'], e.style['strokeWidth']
        (3, 3, 3)
        >>> e.h = 20
        >>> e.h, e.style['h'], e.style['strokeWidth']
        (20, 20, 20)
        """
        return self.css('strokeWidth', 0)
    def _set_h(self, h):
        self.style['h'] = self.style['strokeWidth'] = h # Overwrite style from here.
    h = property(_get_h, _set_h)

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin):
        u"""Build the Ruler in the current context

        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.document import Document
        >>> c = DrawBotContext()
        >>> w, h = 300, 400
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> e = Ruler(parent=page, x=0, y=20, w=page.w, h=3)
        >>> e.build(doc.getView(), (0, 0))
        >>> e.xy
        (0, 20)
        >>> e.size
        (300, 3, 1)
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
        >>> e.build(doc.getView(), (0, 0))
        >>> e.xy
        (0, 20)
        >>> e.size
        (300, 3, 1)
        """
        context = self.context # Get current context and builder.

        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = self._applyAlignment(p) # Ignore z-axis for now.
        sIndent = self.css('indent')
        sTailIndent = self.css('tailIndent')
        w = self.w - sIndent - sTailIndent
 
        if self.drawBefore is not None: # Call if defined
            self.drawBefore(view, p)

        context.setFillColor(None)
        context.setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        context.line((px + sIndent, py), (px + w, py))

        # If there are child elements, recursively draw them over the pixel image.
        self.buildChildElements(view, origin)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin)
      
    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None):
        u"""Build the Ruler in the current context

        >>> from pagebot.contexts.htmlcontext import HtmlContext
        >>> from pagebot.document import Document
        >>> c = HtmlContext()
        >>> doc = Document(w=300, h=400, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> e = Ruler(parent=page, x=0, y=20, w=page.w, h=3)
        >>> e.build(doc.getView(), (0, 0))
        >>> e.xy
        (0, 20)
        >>> e.size
        (300, 3, 1)
        >>> view = doc.getView()
        >>> e.build_html(view, (0, 0))
        """

        context = self.context # Get current context and builder.
        b = context.b # This is a bit more efficient than self.b once we got context
 
        self.build_css(view)
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)    
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        context.setFillColor(None)
        context.setStrokeColor(self.css('stroke', NO_COLOR), self.css('strokeWidth'))
        #b.line((px + sIndent, py), (px + w, py))

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        b.hr(class_=self.class_)

        self.buildChildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        #view.drawElementMetaInfo(self, origin)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
