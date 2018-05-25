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
from pagebot.constants import JUSTIFIED
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance

class Stacked(Group): 
    u"""Showing the specified (variable) font as full pages of stacked adjusted lines.

    """
    BODY_SIZE = 11
    NAME_SIZE = 24
    RLEADING = 0.3 # Points between stacked pixel bounds
    MAX_LEADING = 4
    GUTTER = 12

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
        >>> font = findFont('RobotoDelta-VF')
        >>> #font = findFont('AmstelvarAlpha-VF')
        >>> stacked = Stacked(font, x=m, y=m, w=w-2*m, h=h-2*m, parent=page, context=c)
        >>> doc.export('_export/%sStacked.pdf' % font.info.familyName)
        """
        assert w and h # Make sure there is a size defined.
        Group.__init__(self, w=w, h=h, **kwargs)
        c = self.context
        blurb = Blurb() # Random content creator
        self.f = f # Font instance
        # Add semi-random generated content, styles of fitting.
        x = 0
        y = self.h
        for n in range(100): # As long as they fit in height
            if n == 0: # Some large headline thing
                s = blurb.getBlurb('news_headline', cnt=2, charCnt=10).upper()
                x, y = self.buildStackedLine(s, x, y, wght=1, wdth=-0.3)

            elif n == 1: # Some large headline thing
                s = blurb.getBlurb('design_headline', cnt=2, charCnt=16).upper()
                x, y = self.buildStackedLine(s, x, y, wght=0.3)

            elif n == 2: # Some large headline thing
                s = blurb.getBlurb('design_headline', cnt=3, charCnt=18)
                x, y = self.buildStackedLine(s, x, y, wght=0.9, wdth=-0.4)
                y -= 6

            elif n == 3: # Body text 16/24
                P = 16
                L = 1.5*P
                s = blurb.getBlurb('da_text', cnt=20)
                instance = self.getInstance(wght=0, wdth=0, opsz=P)
                style = dict(font=instance.path, fontSize=P, leading=L, 
                    hyphenation='en', xTextAlign=JUSTIFIED)
                bs = c.newString(s, style=style)
                tw, th = bs.textSize(w=self.w)
                newTextBox(bs, x=x, y=y-th-12, w=self.w, parent=self)
                y -= th+12

            elif n == 4: # Body text 12/18
                P = 12
                L = 1.5*P
                s = blurb.getBlurb('da_text', cnt=60)
                instance = self.getInstance(wght=0, wdth=0, opsz=P)
                style = dict(font=instance.path, fontSize=P, leading=L, 
                    hyphenation='en', xTextAlign=JUSTIFIED)
                bs = c.newString(s, style=style)
                tw, th = bs.textSize(w=self.w)
                newTextBox(bs, x=x, y=y-th-12, w=self.w, parent=self)
                y -= th+12

            elif n == 5: # Body text 10/15
                P = 10
                L = 1.5*P
                s = blurb.getBlurb('design_headline')
                instance = self.getInstance(wght=0.56, wdth=0, opsz=P)
                style = dict(font=instance.path, fontSize=P, leading=L, 
                    hyphenation='en', xTextAlign=JUSTIFIED)
                bs = c.newString(s, style=style)

                s = blurb.getBlurb('da_text', cnt=60)
                instance = self.getInstance(wght=0, wdth=0, opsz=P)
                style = dict(font=instance.path, fontSize=P, leading=L, 
                    hyphenation='en', xTextAlign=JUSTIFIED)
                bs += c.newString(s, style=style)
                tw, th = bs.textSize(w=self.w)
                newTextBox(bs, x=x, y=y-th-12, w=self.w, parent=self)
                y -= th+12

            elif n == 6: # Body test 9/13.5
                P = 9
                L = 1.5*P
                s = blurb.getBlurb('design_headline')
                instance = self.getInstance(wght=0.56, wdth=0, opsz=P)
                style = dict(font=instance.path, fontSize=P, leading=L, 
                    hyphenation='en', xTextAlign=JUSTIFIED)
                bs = c.newString(s, style=style)

                s = blurb.getBlurb('da_text')
                instance = self.getInstance(wght=0, wdth=0, opsz=P)
                style = dict(font=instance.path, fontSize=P, leading=L, xTextAlign=JUSTIFIED)
                bs += c.newString((' '+s)*5, style=style)

                cw = self.w/2-self.GUTTER/2
                tw, th = bs.textSize(w=cw)
                newTextBox(bs, x=x, y=0, h=y-12, w=cw, parent=self)

            elif n == 7: # Body test 10/15
                P = 8
                L = 1.5*P
                s = blurb.getBlurb('design_headline')
                instance = self.getInstance(wght=0.56, wdth=0, opsz=P)
                style = dict(font=instance.path, fontSize=P, leading=L, 
                    hyphenation='en', xTextAlign=JUSTIFIED)
                bs = c.newString(s, style=style)

                s = blurb.getBlurb('da_text')
                instance = self.getInstance(wght=0, wdth=0, opsz=P)
                style = dict(font=instance.path, fontSize=P, leading=L, 
                    hyphenation='en', xTextAlign=JUSTIFIED)
                bs += c.newString((' '+s)*5, style=style)

                cw = self.w/2-self.GUTTER/2
                tw, th = bs.textSize(w=cw)
                newTextBox(bs, x=x+cw+self.GUTTER, y=0, h=y-12, w=cw, parent=self)

            if y < 0:
                break

        #print(self.f.axes.keys())

    def getAxisValue(self, tag, value):
        if not tag in self.f.axes:
            return 0
        minValue, defaultValue, maxValue = self.f.axes[tag]
        if not value:
            return defaultValue
        if value < 0:
            return defaultValue - (defaultValue - minValue)*value
        # else wdth > 0:
        return defaultValue + (maxValue - defaultValue)*value

    def getInstance(self, wght=None, wdth=None, opsz=None):
        u"""Answer the instance of self, corresponding to the normalized location.
        (-1, 0, 1) values for axes.
        """
        # Get real axis values.
        wght = self.getAxisValue('wght', wght)        
        wdth = self.getAxisValue('wdth', wdth)        

        # Make location dictionary
        location = dict(wght=wght, wdth=wdth, opsz=opsz)
        # Return the instance font at this location. The font is stored as file,
        # so it correspondents to normal instance.path behavior,
        return getVarFontInstance(self.f, location)

    def buildStackedLine(self, s, x, y, wght=None, wdth=None):
        u"""Add a textbox to self that fits the string s for the instance indicated by
        the locations-axis values. Then answer the position of the stacked boxes
        based on the bounds of the pixels (not the bounds of the em).
        """
        c = self.context
        # Get the instance for this location. 
        instance = self.getInstance(wght=wght, wdth=wdth)
        style = dict(font=instance.path)
        stackLine = c.newString(s, style=style, w=self.w)
        tx, ty, tw, th = stackLine.bounds()
        # TODO: Fix baseline problem with textbox
        #print(stackLine.fittingFontSize, tx, ty, tw, th)
        y = y - th - min(self.MAX_LEADING, stackLine.fittingFontSize*self.RLEADING)
        newTextBox(stackLine, x=tx, y=y, w=self.w, parent=self)
        return x, y-ty


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
