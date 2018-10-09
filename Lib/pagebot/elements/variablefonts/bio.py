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
#     bio.py
#
from pagebot.elements import TextBox
from pagebot.toolbox.units import em

class Bio(TextBox):
    """Showing the specified (variable) font with its name as headline
    with the bio text about the font.

    """
    BODY_SIZE = 11

    def __init__(self, f, foundryName=None, description=None, foundryStyle=None,
            fontNameStyle=None, bodyStyle=None, **kwargs):
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
        >>> font = findFont('AmstelvarAlpha-VF')
        >>> foundryName = 'Google Fonts'
        >>> description = blurb.getBlurb('article', newLines=True, cnt=120)
        >>> bio = Bio(font, x=m, w=w-2*m, foundryName=foundryName, description=description, parent=page, context=c)
        >>> tw, th = bio.getTextSize()
        >>> bio.y = (h - th)*2/3
        >>> doc.export('_export/TypeNetworkBio.pdf')
        """
        TextBox.__init__(self, '', **kwargs)

        c = self.context
        if foundryStyle is None:
            foundryStyle = dict(font=f.path, fontSize=self.BODY_SIZE, leading=em(0.6))
        if fontNameStyle is None:
            fontNameStyle = dict(font=f.path, leading=em(1.9))
        if bodyStyle is None:
            bodyStyle = dict(font=f.path, fontSize=self.BODY_SIZE, leading=em(1.4))

        self.f = f # Font instance
        foundryName = foundryName or f.info.designer or 'Unknown foundry'
        familyName = f.info.familyName or 'Unknown family'
        bio = c.newString(foundryName+'\n', style=foundryStyle)
        bio += c.newString(familyName+'\n', style=fontNameStyle, w=self.w*2/3)
        bio += c.newString(description or f.info.description or 'Unknown description ' * 40,
            style=bodyStyle)
        self.bs = bio

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
