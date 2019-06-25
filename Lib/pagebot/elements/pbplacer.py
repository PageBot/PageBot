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
#     placer.py
#
from pagebot.elements.element import Element
from pagebot.toolbox.color import color
from pagebot.toolbox.units import point2D, pt

class Placer(Element):
    """Draw an area showing to be a place holder, e.g. reserved places of images in a template.

    >>> from pagebot.toolbox.units import pt
    >>> from pagebot.contexts.drawbotcontext import DrawBotContext
    >>> from pagebot.document import Document
    >>> c = DrawBotContext()
    >>> w, h = pt(300, 400)
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
    >>> page = doc[1]
    >>> e = Placer(parent=page, x=0, y=20, w=page.w, h=3)
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy
    (0pt, 20pt)
    >>> e.css('fill')
    Color(r=0.5, g=0.5, b=0.5, a=0.5)
    >>> e.size
    (300pt, 3pt)
    >>> view = doc.getView()
    >>> e.build(view, pt(0, 0))

    """

    """ TODO: Make this work in Flat

    >>> from pagebot.contexts.flatcontext import FlatContext
    >>> from pagebot.document import Document
    >>> c = FlatContext()
    >>> doc = Document(w=w, h=h, autoPages=1, padding=30, originTop=False, context=c)
    >>> page = doc[1]
    >>> e = Placer(parent=page, x=0, y=20, w=page.w, h=3)
    >>> # Allow the context to create a new document and page canvas. Normally view does it.
    >>> c.newPage(w, h)
    >>> e.build(doc.getView(), (0, 0))
    >>> e.xy
    (0pt, 20pt)
    >>> e.css('fill')
    Color(r=0.5, g=0.5, b=0.5, a=0.5)
    >>> e.size
    (300pt, 3pt)
    """
    DEFAULT_FILL = color(0.5, 0.5, 0.5, 0.5)

    def __init__(self, fill=None, name=None, drawAfter=None, **kwargs):
        if fill is None:
            fill = self.DEFAULT_FILL
        if name is None:
            name = 'Unnamed Placer'
        if drawAfter is None:
            drawAfter = self._drawNameLabel

        Element.__init__(self, fill=fill, name=name, drawAfter=drawAfter, **kwargs)

    def _drawNameLabel(self, aa, view, p):
        x, y = point2D(p)
        context = self.context
        bs = context.newString(self.name, style=dict(font='Verdana', fontSize=18, 
            textFill=(1, 0, 0)))
        tw, th = bs.size
        M = pt(8)
        context.fill(color(1, 1, 1, 0.6))
        context.rect(x + self.w/2 - tw/2 - M, y + self.h/2 - th/2 - M, tw + 2*M, th + 2*M)
        context.text(bs, (x + self.w/2 - tw/2, y + self.h/2 - th/4))


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
