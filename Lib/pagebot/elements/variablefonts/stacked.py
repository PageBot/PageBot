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
from pagebot.elements import Group, newTextBox
from pagebot.constants import RIGHT
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance

class Stacked(Group): 
    u"""Showing the specified (variable) font as full pages of stacked adjusted lines.

    """
    BODY_SIZE = 11
    NAME_SIZE = 24

    def __init__(self, f, w, h, **kwargs):
        u"""    
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> m = 80
        >>> doc = Document(w=w, h=h, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> font = findFont('AmstelvarAlpha-VF')
        >>> stacked = Stacked(font, x=m, y=m, w=w-2*m, h=h-2*m, parent=page, context=c)
        >>> doc.export('_export/TypeNetworkStacked.pdf')
        """
        assert w and h # Make sure there is a size defined.
        Group.__init__(self, w=w, h=h, **kwargs)
        c = self.context
        blurb = Blurb() # Random content creator
        self.f = f # Font instance
        # Add semi-random generated content, styles of fitting.
        y = self.h
        for n in range(100): # As long as they fit in height
            if n == 0: # Some large headline thing
                wghtMin, wghtDefault, wghtMax = self.f.axes['wght']
                wdthMin, wdthDefault, wdthMax = self.f.axes['wdth']
                location = dict(
                    wght=wghtMax, 
                    wdth=wdthDefault-(wdthDefault-wdthMin)*0.3)
                instance = getVarFontInstance(self.f, location)
                style = dict(font=instance.path)
                s = blurb.getBlurb('news_headline', cnt=2)
                headline = c.newString(s.upper(), style=style, w=self.w)
                tw, th = headline.size()
                y = y - th
                newTextBox(headline, y=y, w=self.w, parent=self)
            elif n == 1: # Some large headline thing
                wghtMin, wghtDefault, wghtMax = self.f.axes['wght']
                wdthMin, wdthDefault, wdthMax = self.f.axes['wdth']
                location = dict(
                    wght=wdthDefault+(wghtMax-wghtDefault)*0.3,
                    wdth=wdthDefault
                )
                instance = getVarFontInstance(self.f, location)
                style = dict(font=instance.path)
                s = blurb.getBlurb('news_headline', cnt=3)
                headline = c.newString(s, style=style, w=self.w)
                tw, th = headline.size()
                y = y - th*0.7
                newTextBox(headline, y=y, w=self.w, parent=self)
            elif n == 3: # Some large headline thing
                wghtMin, wghtDefault, wghtMax = self.f.axes['wght']
                wdthMin, wdthDefault, wdthMax = self.f.axes['wdth']
                location = dict(
                    wght=wdthDefault+(wghtMax-wghtDefault)*0.9,
                    wdth=wdthDefault-(wdthDefault-wdthMin)*0.4
                )
                instance = getVarFontInstance(self.f, location)
                style = dict(font=instance.path)
                s = blurb.getBlurb('news_headline', cnt=5)
                headline = c.newString(s, style=style, w=self.w)
                tw, th = headline.size()
                y = y - th*0.7
                newTextBox(headline, y=y, w=self.w, parent=self)
           

        print(self.f.axes.keys())


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
