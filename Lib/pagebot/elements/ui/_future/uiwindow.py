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
#     button.py
#
from pagebot.elements.element import Element
from pagebot.constants import *

class UIWindow(Element):
    """
    """
    def __init__(self, callback=None, minW=None, maxW=None, minH=None, maxH=None,
            closable=None, **kwargs):
        Element.__init__(self, closable=None, **kwargs)
        self.callback = callback
        self.minW = minW or 1
        self.maxW = maxW or XXXL
        self.minH = minH or 1
        self.maxH = maxH or XXXL
        if closable is None:
            closable = True
        self.closable = closable

    def build(self, view, nsParent=None, **kwargs):
        """Draw a button and connect it to a callback function.
        """
        assert nsParent is not None
        self.window = self.context.window(title=self.title, x=self.x, y=self.y,
            w=self.w, h=self.h,
            minW=self.minW, maxW=self.maxW, minH=self.minH, maxH=self.maxH,
            closable=self.closable)
        setattr(nsParent, self.name or 'untitledWindow', self.window)
        for e in self.elements:
            e.build(view, nsParent=self.window)

    def open(self):
        self.window.open()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
