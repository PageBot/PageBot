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

class Window(Element):
    """
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> context = DrawBotContext()
        >>> def buttonCallback(sender):
        ...     print('Callback of', sender)
        >>> e = Button(w=100, h=24, name='My Button', callback=buttonCallback, context=context)
        >>> e
        <Button:My Button (0pt, 0pt, 100pt, 24pt)>
        >>> e.mouseDown('aSender')
        Callback of aSender
    """
    def __init__(self, callback=None, minX=None, maxX=None, minH=None, maxH=None,
        **kwargs):
        Element.__init__(self, closable=None, **kwargs)
        self.callback = callback
        self.minW = minW or 1
        self.maxW = maxW or XXXL
        self.minH = minH or 1
        self.maxH = maxH or XXXL
        if closable is None:
            closable = True
        self.closable = closable

    def mouseDown(self, sender=None):
        if self.callback is not None:
            self.callback(sender)

    def build(self, view, drawElements=True, nsParent=None, **kwargs):
        """Draw a button and connect it to a callback function.
        """
        self.window = self.context.window() = Window((800, 600), minSize=(self.minX, self.minH), 
            maxSize=(self.maxX, self.maxH), closable=self.closable)
        if drawElements:
            for e in self.elements:
                e.build(view, nsParent=self.window)
        


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
