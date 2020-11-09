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
from pagebot.constants import LEFT
from pagebot.elements.element import Element
from pagebot.toolbox.units import asFormatted
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance

class BaseFontShow(Element):
    """Abstract base class for elements that show aspects, values,
    info-graphics and specimes of a font instance of Variable Font."""
    DEFAULT_LABEL_SIZE = 7

    def getTextStyle(self, font, fontSize=None, alignment=None, leading=None):
        """Answers a copy of self.style with modified parameters (if
        defined)."""
        # Make a copy of the entire cascading style from self perspective
        style = self.getFlattenedStyle()
        style['font'] = font.path
        if fontSize is not None:
            style['fontSize'] = fontSize
        if leading is not None:
            style['leading'] = leading
        if alignment is not None:
            style['xTextAlign'] = alignment
        return style

    def getInstance(self, vf=None, location=None):
        """Returns the instance font at this location. The font is stored as a
        file, so it corresponds to normal instance.path behavior."""
        vf = vf or self.f

        if not vf.axes:
            return {}

        if vf and vf.axes:
            return getVarFontInstance(vf, location)
        return vf

    def getAxisValue(self, vf, tag, value):
        """Answers the scaled value for the "tag" axis, where value (-1..0..1)
        is upscaled to ratio in (minValue, defaultValue, maxValue)."""
        if not tag in vf.axes:
            return None
        minValue, defaultValue, maxValue = vf.axes[tag]
        if not value:
            return defaultValue
        if value < 0: # Realative scale between minValue and default
            return defaultValue + (defaultValue - minValue)*value
        # else wdth > 0:  Relative scale between default and maxValue
        return defaultValue + (maxValue - defaultValue)*value

    def getLocation(self, vf=None, wght=None, wdth=None, opsz=None):
        """Answers the instance of self, corresponding to the normalized location.
        (-1, 0, 1) values for axes [wght] and [wdth].
        The optical size [opsz] is supposed to contain the font size, so it is not normalized.
        If [opsz] is not defined, then set it to default, if the axis exist.
        """
        vf = vf or self.f

        if not vf.axes:
            return {}

        # Get real axis values.
        wght = self.getAxisValue(vf, 'wght', wght)
        wdth = self.getAxisValue(vf, 'wdth', wdth)

        if not opsz and 'opsz' in vf.axes:
            opsz = vf.axes['opsz'][1] # Use default value

        # Make location dictionary
        return dict(wght=wght, wdth=wdth, opsz=opsz)

    def buildStackedLine(self, s, origin, x, y, w, h=None, fontSize=None,
            wght=None, wdth=None, useOpsz=True):
        """Draws a textbox to self that fits the string s for the instance
        indicated by the locations-axis values, then answers the (x,y) position
        of the next box, based on the bounds of the pixels (not the bounds of
        the em).

        TODO: Make optional h and fontSize used by adjusting the width/XTRA of
        self.f, if it is a Variable Font."""
        ox, oy, _ = origin

        if useOpsz: # Using [opsz] then set to fontSize
            opsz = fontSize
        else:
            opsz = None # Otherwise ignore.

        # Construct the location
        location = self.getLocation(wght=wght, wdth=wdth, opsz=opsz)
        # Get the instance for this location.

        instance = self.getInstance(location=location)
        style = self.getTextStyle(instance, fontSize)
        stackLine = self.context.newString(s, style=style, w=w)
        capHeight = float(instance.info.capHeight) / instance.info.unitsPerEm * stackLine.fontSize
        #tx, ty, tw, th = stackLine.bounds()
        #self.context.text(stackLine, (ox+x-tx, oy+y-capHeight))
        self.context.text(stackLine, (ox+x, oy+y-capHeight))
        return x, y-capHeight-self.gh

    def buildText(self, s1, s2, origin, x, y, w, h, fontSize, alignment=None,
            labelSize=None, label=None, Bwght=0, Bwdth=0, Rwght=0, Rwdth=0,
            useOpsz=True):
        """Makes a new instance for the bold and roman locations (if self.f is
        a Variable Font). Draws a textbox fitting the content ot otherwise
        forced to (w,h) size. Answers the (x, y) position of the next stacked
        block.

        If labelSize defined then show the defaul label: Font family name
        fontSize / leading.
        If label is defined, then use that label in the defined font font size.

        FIXME: bs is a tuple, not BabelString.
        """
        ox, oy, _ = origin

        # Using [opsz] then set to fontSize.
        if useOpsz:
            opsz = fontSize
        else:
            opsz = None # Otherwise ignore.

        # Construct the location.
        location = self.getLocation(opsz=opsz)

        # Get Roman for labels, using default axis values.
        instance = self.getInstance(location=location)

        # Labels by default in default roman, showing font family name,
        # fontSize and rounded leading.
        style = self.getTextStyle(instance, labelSize or self.DEFAULT_LABEL_SIZE, LEFT, 0.8)
        if labelSize is not None and label is None:
            label = '%s %s/%s\n\n' % (self.f.info.familyName,
                asFormatted(fontSize),
                asFormatted(self.css('leading', 0), hasFormat='%0.1f'))
        # Create BabelString/FormattedString if content.
        bs = self.context.newString(label or '', style=style)

        if s1:
            # In case s1 lead is defined, then use that for the bold version of
            # self.f Construct the location.
            location = self.getLocation(wght=Bwght, wdth=Bwdth, opsz=opsz)
            instance = self.getInstance(location=location)
            style = self.getTextStyle(instance, fontSize, alignment)
            # Create BabelString/FormattedString if content.
            bs += self.context.newString((s1 or '')+' ', style=style)

        # Make Roman style. Use font size of [opsz] axis, if it exists.
        # Construct the location
        location = self.getLocation(wght=Rwght, wdth=Rwdth, opsz=opsz)
        instance = self.getInstance(location=location)
        style = self.getTextStyle(instance, fontSize, alignment)
        # Add roman formatted string to what we already had.
        bs += self.context.newString(s2, style=style)
        # Get the text height for the request width.
        tw, th = bs.textSize(w=w)
        # Use h if defined, otherwise text height.
        self.context.textBox(bs, (ox+x, oy+y-(h or th)-self.gh, w, h or th))

        # Answer the new position (x, y) for the next block, using self.gh
        # (gutter height) as distance.
        return x, y-(h or th)-self.gh

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
