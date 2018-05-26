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
#     basefontshow.py
#
from random import choice
from pagebot.elements import Element
from pagebot.constants import JUSTIFIED, LEFT
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.toolbox.transformer import asFormatted

class BaseFontShow(Element): 
    u"""Abstract base class for elements that show aspects, values, info-graphics and
    specimes of a font instance of Variable Font.

    """

    def getTextStyle(self, font, fontSize=None, alignment=None, rLeading=None):
        u"""Answer a copy of self.style with modified parameters (if defined)"""
        # Make a copy of the entire cascading style from self perspective
        style = self.getFlattenedStyle() 
        style['font'] = font.path
        if fontSize is not None:
            style['fontSize'] = fontSize
        if rLeading is not None:
            style['rLeading'] = rLeading
        if alignment is not None:
            style['xTextAlign'] = alignment
        return style

    def getAxisValue(self, tag, value):
        u"""Answer the scaled value for the "tag" axis, where value (-1..0..1) is upscaled to
        ratio in (minValue, defaultValue, maxValue)."""
        if not tag in self.f.axes:
            return 0
        minValue, defaultValue, maxValue = self.f.axes[tag]
        if not value:
            return defaultValue
        if value < 0: # Realative scale between minValue and default
            return defaultValue + (defaultValue - minValue)*value
        # else wdth > 0:  Relative scale between default and maxValue
        return defaultValue + (maxValue - defaultValue)*value

    def getInstance(self, wght=None, wdth=None, opsz=None):
        u"""Answer the instance of self, corresponding to the normalized location.
        (-1, 0, 1) values for axes [wght] and [wdth].
        The optical size [opsz] is supposed to contain the font size, so it is not normalize.
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
        instance = getVarFontInstance(self.f, location)
        return instance

    def buildStackedLine(self, s, origin, x, y, w, h=None, fontSize=None, wght=None, wdth=None):
        u"""Draw a textbox to self that fits the string s for the instance indicated by
        the locations-axis values. 
        Then answer the (x,y) position of the next box, based on the bounds of the pixels 
        (not the bounds of the em).
        TODO: Make optional h and fontSize used by adjusting the width/XTRA of self.f, if it
        is a Variable Font.
        """
        c = self.context
        ox, oy, _ = origin
        # Get the instance for this location. 
        instance = self.getInstance(wght=wght, wdth=wdth)
        style = self.getTextStyle(instance, fontSize)
        stackLine = c.newString(s, style=style, w=w)
        capHeight = float(instance.info.capHeight)/instance.info.unitsPerEm * stackLine.fittingFontSize
        tx, ty, tw, th = stackLine.bounds()
        c.text(stackLine, (ox+x-tx, oy+y-capHeight))
        return x, y-capHeight+ty-self.gh

    def buildStackedText(self, s1, s2, origin, x, y, w, h, fontSize, labelSize, alignment=None, Bwght=0, Bwdth=0, Rwght=0, Rwdth=0):      
        u"""Make a new instance for the bold and roman locations (if self.f is a Variable Font).
        Draw a textbox fitting the content ot otherwise forced to (w,h) size.
        Answer the (x, y) position of the next stacked block.
        """
        c = self.context
        ox, oy, _ = origin

        # Labels by default in default roman, showing font family name, fontSize and rounded leading.
        instance = self.getInstance(opsz=fontSize) # Get Roman for labels, using default axis values.
        style = self.getTextStyle(instance, labelSize or 7, LEFT, 0.8)
        if labelSize:
            label = '%s %s/%s\n\n' % (self.f.info.familyName, 
                asFormatted(fontSize), 
                asFormatted(self.css('leading', 0)+self.css('rLeading', 1)*fontSize, format='%0.1f'))
        else:
            label = ''
        bs = c.newString(label, style=style) # Create BabelString/FormattedString if content.
 
        if s1: # In case s1 lead is defined, then use that for the bold version of self.f
            instance = self.getInstance(wght=Bwght, wdth=Bwdth, opsz=fontSize)
            style = self.getTextStyle(instance, fontSize, alignment)
            bs += c.newString((s1 or '')+' ', style=style) # Create BabelString/FormattedString if content.
 
        # Make Roman style. Use font size of [opsz] axis, if it exists.
        instance = self.getInstance(wght=Rwght, wdth=Rwdth, opsz=fontSize)
        style = self.getTextStyle(instance, fontSize, alignment)
        # Add roman formatted string to what we already had.
        bs += c.newString(s2, style=style) 
        # Get the text height for the request width.
        tw, th = bs.textSize(w=w) 
        c.textBox(bs, (ox+x, oy+y-(h or th)-self.gh, w, h or th)) # Use h if defined, otherwise text height.

        # Answer the new position (x, y) for the next block, using self.gh (gutter height) as distance.
        return x, y-th-self.gh 

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
