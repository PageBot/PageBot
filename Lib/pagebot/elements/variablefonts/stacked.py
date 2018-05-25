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
from pagebot.elements import Element
from pagebot.constants import JUSTIFIED, LEFT
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.toolbox.transformer import pointOffset

class Stacked(Element): 
    u"""Showing the specified (variable) font as full page with a matrix
    of all glyphs in the font.

    """
    V_GUTTER = 12

    def __init__(self, f, **kwargs):
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
        >>> #font = findFont('RobotoDelta-VF')
        >>> font = findFont('AmstelvarAlpha-VF')
        >>> font = findFont('Upgrade-Regular')
        >>> font = findFont('Bitcount_Mono_Double-Line_Circle')
        >>> font = findFont('Bitcount_Mono_Double-Book_Plus')
        >>> font = findFont('Escrow-Bold')
        >>> gs = Stacked(font, x=m, y=m, w=w-2*m, h=h-2*m, gh=6, parent=page, context=c)
        >>> doc.export('_export/%sStacked.pdf' % font.info.familyName)
        """
        Element.__init__(self, **kwargs)
        self.f = f # Font instance


    def build(self, view, origin, drawElements=True):
        u"""Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)
        p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showElementFrame == True
        view.drawElementFrame(self, p) 

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        self.drawStacked(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on flag 'view.showElementInfo'


    def drawStacked(self, view, origin):
        c = self.context
        blurb = Blurb() # Random content creator
        # Add semi-random generated content, styles of fitting.
        x = 0
        y = self.h

        # Top headline. (x,y) is top-left of the box
        s = blurb.getBlurb('news_headline', cnt=2, charCnt=10).upper()
        x, y = self.buildStackedLine(s, origin, x, y, wght=1, wdth=-0.3)

        # Second headline
        s = blurb.getBlurb('design_headline', cnt=2, charCnt=12).upper()
        x, y = self.buildStackedLine(s, origin, x, y, wght=0.3)

        # Some large headline thing
        s = blurb.getBlurb('design_headline', cnt=3, charCnt=12)
        x, y = self.buildStackedLine(s, origin, x, y, wght=0.9, wdth=-0.4)

        L = 1.5
        # Body text 16/24
        s = blurb.getBlurb('da_text', cnt=20)
        x, y = self.buildStackedText(None, s, origin, x, y, self.w, None, 16, L, JUSTIFIED)        

        # Body text 12/18
        s = blurb.getBlurb('da_text', cnt=30)
        x, y = self.buildStackedText(None, s, origin, x, y, self.w, None, 12, L, JUSTIFIED)        

        # Body text 10/15
        s1 = blurb.getBlurb('design_headline')
        s2 = blurb.getBlurb('da_text', cnt=20)
        x, y = self.buildStackedText(s1, s2, origin, x, y, self.w, None, 10, L, JUSTIFIED, Bwght=0.56)        

        # Body text 9/13.5
        s1 = blurb.getBlurb('design_headline')
        s2 = blurb.getBlurb('da_text') + ' ' + blurb.getBlurb('da_text') + ' ' + blurb.getBlurb('da_text')
        x, _ = self.buildStackedText(s1, s2, origin, x, y, (self.w-self.gw)/2, y, 9, L, LEFT, Bwght=0.56)        

        # Body text 8/12
        s1 = blurb.getBlurb('design_headline')
        s2 = blurb.getBlurb('da_text') + ' ' + blurb.getBlurb('da_text') + ' ' + blurb.getBlurb('da_text')
        x, y = self.buildStackedText(s1, s2, origin, x+(self.w+self.gw)/2, y, (self.w-self.gw)/2, y, 8, L, LEFT, Bwght=0.56)        


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
        if not self.f.axes:
            return self.f

        # Get real axis values.
        wght = self.getAxisValue('wght', wght)        
        wdth = self.getAxisValue('wdth', wdth)        

        # Make location dictionary
        location = dict(wght=wght, wdth=wdth, opsz=opsz)
        # Return the instance font at this location. The font is stored as file,
        # so it correspondents to normal instance.path behavior,
        return getVarFontInstance(self.f, location)

    def buildStackedLine(self, s, origin, x, y, wght=None, wdth=None):
        u"""Draw a textbox to self that fits the string s for the instance indicated by
        the locations-axis values. Then answer the (x,y) position of the next box.
        based on the bounds of the pixels (not the bounds of the em).

        """
        c = self.context
        ox, oy, _ = origin
        # Get the instance for this location. 
        instance = self.getInstance(wght=wght, wdth=wdth)
        style = dict(font=instance.path)
        stackLine = c.newString(s, style=style, w=self.w)
        capHeight = float(instance.info.capHeight)/instance.info.unitsPerEm * stackLine.fittingFontSize
        tx, ty, tw, th = stackLine.bounds()
        c.text(stackLine, (ox+x-tx, oy+y-capHeight))
        return x, y-capHeight+ty-self.gh

    def buildStackedText(self, s1, s2, origin, x, y, w, h, fontSize, rLeading, alignment, Bwght=0, Bwdth=0, Rwght=0, Rwdth=0):      
        c = self.context
        ox, oy, _ = origin
        instance = self.getInstance(wght=Bwght, wdth=Bwdth, opsz=fontSize)
        style = dict(font=instance.path, fontSize=fontSize, leading=fontSize*rLeading, 
            hyphenation='en', xTextAlign=alignment)
        bs = c.newString((s1 or '')+' ', style=style)
 
        instance = self.getInstance(wght=Rwght, wdth=Rwdth, opsz=fontSize)
        style = dict(font=instance.path, fontSize=fontSize, leading=fontSize*rLeading, 
            hyphenation='en', xTextAlign=alignment)
        bs += c.newString(s2, style=style)
        tw, th = bs.textSize(w=w)
        c.textBox(bs, (ox+x, oy+y-(h or th)-self.gh, w, h or th))
        return x, y-th+self.gh-self.V_GUTTER

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
