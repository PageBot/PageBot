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
from pagebot.elements import Element
from pagebot.constants import LEFT
from pagebot.toolbox.transformer import asFormatted

class BaseFontShow(Element):
    """Abstract base class for elements that show aspects, values,
    info-graphics and specimes of a font instance of Variable Font."""
    DEFAULT_LABEL_SIZE = 7

    def getTextStyle(self, font, fontSize=None, alignment=None, rLeading=None):
        """Answers a copy of self.style with modified parameters (if
        defined)."""
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

    def buildStackedLine(self, s, origin, x, y, w, h=None, fontSize=None,
            wght=None, wdth=None, useOpsz=True):
        """Draws a textbox to self that fits the string s for the instance
        indicated by the locations-axis values, then answers the (x,y) position
        of the next box, based on the bounds of the pixels (not the bounds of
        the em).

        TODO: Make optional h and fontSize used by adjusting the width/XTRA of
        self.f, if it is a Variable Font."""
        c = self.context
        ox, oy, _ = origin
        if useOpsz: # Using [opsz] then set to fontSize
            opsz = fontSize
        else:
            opsz = None # Otherwise ignore.
        # Construct the location
        location = self.getLocation(wght=wght, wdth=wdth, opsz=opsz)
        # Get the instance for this location.
        instance = self.getInstance(location)
        style = self.getTextStyle(instance, fontSize)
        stackLine = c.newString(s, style=style, w=w)
        capHeight = float(instance.info.capHeight) / instance.info.unitsPerEm * stackLine.fittingFontSize
        tx, ty, tw, th = stackLine.bounds()
        c.text(stackLine, (ox+x-tx, oy+y-capHeight))
        return x, y-capHeight+ty-self.gh

    def buildTextBox(self, s1, s2, origin, x, y, w, h, fontSize, alignment=None,
            labelSize=None, label=None, Bwght=0, Bwdth=0, Rwght=0, Rwdth=0, useOpsz=True):
        """Makes a new instance for the bold and roman locations (if self.f is
        a Variable Font). Draws a textbox fitting the content ot otherwise
        forced to (w,h) size. Answers the (x, y) position of the next stacked
        block.

        If labelSize defined then show the defaul label: Font family name
        fontSize/leading.
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
        instance = self.getInstance(location) # Get Roman for labels, using default axis values.
        # Labels by default in default roman, showing font family name, fontSize and rounded leading.
        style = self.getTextStyle(instance, labelSize or self.DEFAULT_LABEL_SIZE, LEFT, 0.8)
        if labelSize is not None and label is None:
            label = '%s %s/%s\n\n' % (self.f.info.familyName,
                asFormatted(fontSize),
                asFormatted(self.css('leading', 0)+self.css('rLeading', 1)*fontSize, format='%0.1f'))
        bs = c.newString(label or '', style=style) # Create BabelString/FormattedString if content.

        if s1:
            # In case s1 lead is defined, then use that for the bold version of
            # self.f Construct the location.
            location = self.getLocation(wght=Bwght, wdth=Bwdth, opsz=opsz)
            instance = self.getInstance(location)
            style = self.getTextStyle(instance, fontSize, alignment)
            bs += c.newString((s1 or '')+' ', style=style) # Create BabelString/FormattedString if content.

        # Make Roman style. Use font size of [opsz] axis, if it exists.
        # Construct the location
        location = self.getLocation(wght=Rwght, wdth=Rwdth, opsz=opsz)
        instance = self.getInstance(location)
        style = self.getTextStyle(instance, fontSize, alignment)
        # Add roman formatted string to what we already had.
        bs += c.newString(s2, style=style)
        # Get the text height for the request width.
        tw, th = bs.textSize(w=w)
        c.textBox(bs, (ox+x, oy+y-(h or th)-self.gh, w, h or th)) # Use h if defined, otherwise text height.

        # Answer the new position (x, y) for the next block, using self.gh
        # (gutter height) as distance.
        return x, y-(h or th)-self.gh

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
