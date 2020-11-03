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
#     uibutton.py
#
from pagebot.elements.element import Element

class UIButton(Element):
    """
        >>> from pagebot import getContext
        >>> context = getContext()
        >>> def buttonCallback(sender):
        ...     print('Callback of', sender)
        >>> e = UIButton(w=100, h=24, name='My Button', callback=buttonCallback, context=context)
        >>> e
        <UIButton "My Button" w=100pt h=24pt>
    """
    def __init__(self, callback=None, **kwargs):
        Element.__init__(self, **kwargs)
        self.callback = callback

    def build(self, view, nsParent=None, **kwargs):
        """Draw a button and connect it to a callback function.
        """
        assert nsParent is not None
        button = self.context.button(title=self.title, x=self.x, y=self.y,
            w=self.w, h=self.h, style=self.style, callback=self.callback)
        print('dsdadas', button, self.callback)
        setattr(nsParent, self.name or 'untitledButton', button)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
