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
#     oval.py
#


from pagebot.constants import ORIGIN
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import noColor
from pagebot.constants import DEFAULT_WIDTH, DEFAULT_HEIGHT, ORIGIN

class Oval(Element):

    #   G E N E R I C  C O N T E X T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True):
        """Draw the oval in the current context canvas.

        >>> e = Oval(x=0, y=20, w=500, h=3)
        >>> e.xy
        (0pt, 20pt)
        >>> e.size
        (500pt, 3pt)
        """
        context = self.context # Get current context and builder.
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        #self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case
        # view.showFrame == True
        view.drawElementFrame(self, p)

        if self.drawBefore is not None:
            # Call if defined
            self.drawBefore(self, view, p)

        context.fill(self.css('fill', noColor))
        context.stroke(self.css('stroke', noColor), self.css('strokeWidth'))
        context.oval(px, py, self.w, self.h)

        if drawElements:
            self.buildChildElements(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin)

class Circle(Oval):
    def __init__(self, r=None, x=None, y=None, w=None, h=None, **kwargs):
        """Draw the oval in the current context canvas.

        >>> from pagebot.toolbox.units import pt
        >>> e = Circle(r=pt(30))
        >>> e.xy, e.size
        ((-30pt, -30pt), (60pt, 60pt))
        """
        if r is not None:
            w = h = 2*r
        x = (x or ORIGIN[0]) - (w or DEFAULT_WIDTH)/2
        y = (y or ORIGIN[1]) - (h or DEFAULT_HEIGHT)/2
        Oval.__init__(self, x=x, y=y, w=w, h=h, **kwargs)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
