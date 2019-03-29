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

class Button(Element):
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
    def __init__(self, callback=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.callback = callback

    def mouseDown(self, sender=None):
        if self.callback is not None:
            self.callback(sender)

    def build(self, view, nsParent=None, **kwargs):
        """Draw a button and connect it to a callback function.
        """
        setattr(nsParent, self.name, buttong)
        button = self.context.button(title=self.title, x=self.x, y=self.y, w=self.w, h=self.h, 
            style=self.style, callback=self.callback)
        
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
