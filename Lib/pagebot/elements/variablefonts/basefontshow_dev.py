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
#     basefontshow.py
#
#     Under development, make these into global functions
#     And then connect specimen elements again.

from pagebot.elements import Element
from pagebot.constants import LEFT
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.toolbox.units import asFormatted

class BaseFontShow(Element): 
    """Abstract base class for elements that show aspects, values, info-graphics and
    specimes of a font instance of Variable Font.

    """
    DEFAULT_LABEL_SIZE = 7

    def getTextStyle(self, vf, fontSize=None, alignment=None, leading=None):
        """Answers a copy of self.style with modified parameters (if defined)"""
        # Make a copy of the entire cascading style from self perspective
        style = self.getFlattenedStyle() 
        style['font'] = vf.path
        if fontSize is not None:
            style['fontSize'] = fontSize
        if leading is not None:
            style['leading'] = leading
        if alignment is not None:
            style['xTextAlign'] = alignment
        return style

    def getAxisValue(self, vf, tag, value):
        """Answers the scaled value for the "tag" axis, where value (-1..0..1) is upscaled to
        ratio in (minValue, defaultValue, maxValue)."""
        if not tag in vf.axes:
            return None
        minValue, defaultValue, maxValue = self.f.axes[tag]
        if not value:
            return defaultValue
        if value < 0: # Realative scale between minValue and default
            return defaultValue + (defaultValue - minValue)*value
        # else wdth > 0:  Relative scale between default and maxValue
        return defaultValue + (maxValue - defaultValue)*value

    def getLocation(self, vf, wght=None, wdth=None, opsz=None):
        """Answers the instance of self, corresponding to the normalized location.
        (-1, 0, 1) values for axes [wght] and [wdth].
        The optical size [opsz] is supposed to contain the font size, so it is not normalized.
        If [opsz] is not defined, then set it to default, if the axis exist.
        """
        if not self.f.axes:
            return {}

        # Get real axis values.
        wght = self.getAxisValue('wght', wght)        
        wdth = self.getAxisValue('wdth', wdth)        

        if not opsz and 'opsz' in vf.axes:
            opsz = vf.axes['opsz'][1] # Use default value

        # Make location dictionary
        return dict(wght=wght, wdth=wdth, opsz=opsz)

    def buildStackedLine(self, vf, s, origin, x, y, w, h=None, fontSize=None, wght=None, wdth=None, useOpsz=True):
        """Draw a textbox to self that fits the string s for the instance indicated by
        the locations-axis values. 
        Then answer the (x,y) position of the next box, based on the bounds of the pixels 
        (not the bounds of the em).
        TODO: Make optional h and fontSize used by adjusting the width/XTRA of self.f, if it
        is a Variable Font.
        """
        c = self.context
        ox, oy, _ = origin
        if useOpsz: # Using [opsz] then set to fontSize
            opsz = fontSize
        else:
            opsz = None # Otherwise ignore.
        # Construct the location
        location = self.getLocation(wght=wght, wdth=wdth, opsz=opsz)
        # Get the instance for this location. 
        instance = getVarFontInstance(vf, location)
        style = self.getTextStyle(instance, fontSize)
        stackLine = c.newString(s, style=style, w=w)
        capHeight = float(instance.info.capHeight)/instance.info.unitsPerEm * stackLine.fittingFontSize
        tx, ty, tw, th = stackLine.bounds()
        c.text(stackLine, (ox+x-tx, oy+y-capHeight))
        return x, y-capHeight+ty-self.gh

    def buildTextBox(self, s1, s2, origin, x, y, w, h, vf, fontSize, alignment=None, 
            labelSize=None, label=None, Bwght=0, Bwdth=0, Rwght=0, Rwdth=0, useOpsz=True):      
        """Make a new instance for the bold and roman locations (if self.f is a Variable Font).
        Draw a textbox fitting the content ot otherwise forced to (w,h) size.
        Answer the (x, y) position of the next stacked block.

        If labelSize defined then show the defaul label: Font family name fontSize/leading
        If label is defined, then use that label in the defined font font size.
        """
        c = self.context
        ox, oy, _ = origin
        if useOpsz: # Using [opsz] then set to fontSize
            opsz = fontSize
        else:
            opsz = None # Otherwise ignore.
        # Construct the location
        location = self.getLocation(opsz=opsz)
        instance = getVarFontInstance(vf, location) # Get Roman for labels, using default axis values.
        # Labels by default in default roman, showing font family name, fontSize and rounded leading.
        style = self.getTextStyle(instance, labelSize or self.DEFAULT_LABEL_SIZE, LEFT, 0.8)
        if labelSize is not None and label is None:
            label = '%s %s/%s\n\n' % (vf.info.familyName, 
                asFormatted(fontSize), 
                asFormatted(self.css('leading', 0), format='%0.1f'))
        bs = c.newString(label or '', style=style) # Create BabelString/FormattedString if content.
 
        if s1: # In case s1 lead is defined, then use that for the bold version of self.f
            # Construct the location
            location = self.getLocation(wght=Bwght, wdth=Bwdth, opsz=opsz)
            instance = self.getInstance(location)
            style = self.getTextStyle(instance, fontSize, alignment)
            bs += c.newString((s1 or '')+' ', style=style) # Create BabelString/FormattedString if content.
 
        # Make Roman style. Use font size of [opsz] axis, if it exists.
        # Construct the location
        location = self.getLocation(wght=Rwght, wdth=Rwdth, opsz=opsz)
        instance = getVarFontInstance(vf, location)
        style = self.getTextStyle(instance, fontSize, alignment)
        # Add roman formatted string to what we already had.
        bs += c.newString(s2, style=style) 
        # Get the text height for the request width.
        tw, th = bs.textSize(w=w) 
        c.textBox(bs, (ox+x, oy+y-(h or th)-self.gh, w, h or th)) # Use h if defined, otherwise text height.

        # Answer the new position (x, y) for the next block, using self.gh (gutter height) as distance.
        return x, y-(h or th)-self.gh 

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
