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
#     line.py
#
from pagebot.elements.element import Element
from pagebot.constants import ORIGIN
from pagebot.toolbox.units import units, pointOffset

class Line(Element):
    """Draws a straight horizontal ruler."""

    def _get_w(self):
        """Answers the width of the Line element.

        >>> e = Line(w=100)
        >>> e.w
        100pt
        >>> e = Line(w=0)
        >>> e.w
        0pt
        """
        base = dict(base=self.parentW, em=self.em) # In case relative units, use this as base.
        return units(self.css('w', 0), base=base)

    def _set_w(self, w):
        self.style['w'] = units(w) # Overwrite element local style from here, parent css becomes inaccessable.

    w = property(_get_w, _set_w)

    def _get_h(self):
        """Answers the height of the Line element.

        >>> e = Line(h=100)
        >>> e.h
        100pt
        >>> e = Line(h=0)
        >>> e.h
        0pt
        """
        base = dict(base=self.parentH, em=self.em) # In case relative units, use this as base.
        return units(self.css('h', 0), base=base)

    def _set_h(self, h):
        self.style['h'] = units(h) # Overwrite element local style from here, parent css becomes inaccessable.

    h = property(_get_h, _set_h)

    #   D R A W B O T / F L A T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True, **kwargs):
        """Draw a line on the current context canvas.

        >>> from pagebot.toolbox.units import pt
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.document import Document
        >>> c = DrawBotContext()
        >>> w, h = pt(300, 400)
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> e = Line(parent=page, x=0, y=20, w=page.w, h=0)
        >>> e.x, e.y, e.w, e.h
        (0pt, 20pt, 300pt, 0pt)
        >>> e.build(doc.getView(), pt(0, 0))
        >>> e.xy
        (0pt, 20pt)
        >>> e.size
        (300pt, 0pt)
        >>> view = doc.getView()
        >>> e.build(view, pt(0, 0))

        >>> from pagebot.contexts.flatcontext import FlatContext
        >>> from pagebot.document import Document
        >>> c = FlatContext()
        >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> e = Line(parent=page, x=0, y=20, w=page.w, h=3)
        >>> # Allow the context to create a new document and page canvas. Normally view does it.
        >>> c.newPage(w, h)
        >>> e.build(doc.getView(), (0, 0))
        >>> e.xy
        (0pt, 20pt)
        >>> e.size3D
        (300pt, 3pt, 100pt)
        """
        context = self.context # Get current context and builder.
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.
        s = self.stroke
        w = self.strokeWidth

        context.stroke(s, w)
        context.line((px, py), (px + self.w, py + self.h))

        # Let the view draw frame info for debugging, in case view.showFrame == True
        view.drawElementFrame(self, p)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        if drawElements:
            # If there are child elements, recursively draw them over the pixel image.
            self.buildChildElements(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin)

    #   H T M L  /  C S S  S U P P O R T

    def build_html(self, view, origin=None, drawElements=True, **kwargs):

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view)

        if drawElements:
            self.drawChildElements(view, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view)

        self._restoreScale(view)
        view.drawElementInfo(self, origin)


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
