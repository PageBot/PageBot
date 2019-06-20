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
#	  title.py
#
from pagebot.elements import TextBox
from pagebot.constants import RIGHT
from pagebot.toolbox.units import em

class Title(TextBox): 
    """Showing the specified (variable) font with its name as headline 
    and designer name.

    """
    BODY_SIZE = 11
    NAME_SIZE = 24

    def __init__(self, f, foundryName=None, designer=None, foundryStyle=None, 
            fontNameStyle=None, designerStyle=None, **kwargs):
        """    
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
        >>> #font = findFont('RobotoDelta-VF')
        >>> font = findFont('AmstelvarAlpha-VF')
        >>> foundryName = 'Google Fonts'
        >>> designer = 'David Berlow'
        >>> title = Title(font, x=m, w=w-2*m, foundryName=foundryName, designer=designer, parent=page, context=c)
        >>> tw, th = title.getTextSize()
        >>> title.y = (h - th)*2/3
        >>> doc.export('_export/%sTitle.pdf' % font.info.familyName)
        """
        TextBox.__init__(self, '', **kwargs)

        c = self.context
        if foundryStyle is None:
            foundryStyle = dict(font=f.path, fontSize=self.BODY_SIZE, leading=em(0.6))
        if fontNameStyle is None:
            fontNameStyle = dict(font=f.path, leading=em(1.9))
        if designerStyle is None:
            designerStyle = dict(font=f.path, fontSize=self.NAME_SIZE, leading=em(1.4), xTextAlign=RIGHT)

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
