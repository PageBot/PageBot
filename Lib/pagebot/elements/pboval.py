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


from pagebot.constants import ORIGIN, MIDDLE, CENTER
from pagebot.elements.element import Element
from pagebot.toolbox.units import pointOffset
from pagebot.toolbox.color import noColor
from pagebot.constants import ORIGIN

class Oval(Element):

    #   G E N E R I C  C O N T E X T  S U P P O R T

    def build(self, view, origin=ORIGIN, drawElements=True, **kwargs):
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
            self.buildChildElements(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin)

class Circle(Oval):
    def __init__(self, r=None, x=None, y=None, w=None, h=None, 
            xAlign=None, yAlign=None, **kwargs):
        """Draw the oval in the current context canvas.

        >>> from pagebot.toolbox.units import pt
        >>> e = Circle(r=pt(30))
        >>> e.xy, e.size
        ((0pt, 0pt), (60pt, 60pt))
        >>> e.box, e.top, e.right, e.bottom, e.left
        ((0pt, 0pt, 60pt, 60pt), 0pt, 30pt, 0pt, -30pt)
        """
        if r is not None:
            w = h = 2*r
        if x is None:
            x = ORIGIN[0]
        if y is None:
            y = ORIGIN[1]
        Oval.__init__(self, x=x, y=y, w=w, h=h, xAlign=xAlign or CENTER, yAligh=yAlign or MIDDLE, **kwargs)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
