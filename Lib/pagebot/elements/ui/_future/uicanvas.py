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
#     uicanvas.py
#
from pagebot.elements.element import Element

class UICanvas(Element):

    def build(self, view, nsParent=None, **kwargs):
        """Draw a button and connect it to a callback function.
        """
        assert nsParent is not None
        canvas = self.context.canvas(x=self.x, y=self.y, w=self.w, h=self.h)
        setattr(nsParent, self.name or 'untitledCanvas', canvas)
        
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
