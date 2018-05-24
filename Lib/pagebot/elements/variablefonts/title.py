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
#	  title.py
#
from pagebot.elements import TextBox
from pagebot.constants import RIGHT
from pagebot.toolbox.transformer import pointOffset

class Title(TextBox): 
    u"""Showing the specified (variable) font with its name as headline 
    and designer name.

    """
    BODY_SIZE = 11
    NAME_SIZE = 24

    def __init__(self, f, foundryName=None, designer=None, foundryStyle=None, 
            fontNameStyle=None, designerStyle=None, **kwargs):
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
        >>> foundryName = 'Google Fonts'
        >>> designer = blurb.getBlurb('name')
        >>> title = Title(font, x=m, w=w-2*m, foundryName=foundryName, designer=designer, parent=page, context=c)
        >>> tw, th = title.getTextSize()
        >>> title.y = (h - th)*2/3
        >>> doc.export('_export/TypeNetworkTitle.pdf')
        """
        TextBox.__init__(self, '', **kwargs)

        c = self.context
        if foundryStyle is None:
            foundryStyle = dict(font=f.path, fontsize=self.BODY_SIZE, rLeading=0.6)
        if fontNameStyle is None:
            fontNameStyle = dict(font=f.path, rLeading=1.9)
        if designerStyle is None:
            designerStyle = dict(font=f.path, fontsize=self.NAME_SIZE, rLeading=1.4, xTextAlign=RIGHT)

        self.f = f # Font instance
        foundryName = foundryName or f.info.designer or 'Unknown foundry'
        familyName = f.info.familyName or 'Unknown family'
        designerName = 'by ' + designer or f.info.designer or 'Unknown designer'

        title = c.newString(foundryName+'\n', style=foundryStyle)
        title += c.newString(familyName+'\n', style=fontNameStyle, w=self.w)
        title += c.newString(designerName, style=designerStyle)
        self.bs = title

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
