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
#     stacked.py
#
from pagebot.elements import TextBox
from pagebot.constants import RIGHT
from pagebot.toolbox.transformer import pointOffset

class Stacked(TextBox): 
    u"""Showing the specified (variable) font as full pages of stacked adjusted lines.

    """
    BODY_SIZE = 11
    NAME_SIZE = 24

    def __init__(self, f, **kwargs):
        u"""    
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.contributions.filibuster.blurb import Blurb
        >>> blurb = Blurb()
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> m = 80
        >>> doc = Document(w=w, h=h, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> font = findFont('Amstelvar-Roman-VF')
        >>> title = Stacked(font, x=m, w=w-2*m, parent=page, context=c)
        >>> doc.export('_export/TypeNetworkStacked.pdf')
        """
        TextBox.__init__(self, '', **kwargs)

        c = self.context

        self.f = f # Font instance
        print(f.axes)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
