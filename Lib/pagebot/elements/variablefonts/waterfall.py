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
#     waterfall.py
#
from pagebot.elements import TextBox
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.toolbox.units import em, asFormatted, pt

class Waterfall(TextBox):
    """Showing the specified (variable) font as waterfall.

    """
    SAMPLE = 'Jabberwocky'

    def __init__(self, f, showLabel=True, labelSize=7, sampleText=None, factor=0.9, location=None, useOpsz=True, **kwargs):
        """
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter, RIGHT
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> from pagebot.toolbox.color import color        
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> style = dict(fill=color(0.95), leading=em(1.3), fontSize=48, xTextAlign=RIGHT)
        >>> conditions = [Fit()] # FIX: Does not seem to work for TextBox
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF')
        >>> loc = dict(wght=1)
        >>> useOpsz = False
        >>> page.pw, page.w, 500
        (6.28", 8.50", 500)
        >>> gs = Waterfall(font1, parent=page, conditions=conditions, padding=20, style=style, w=page.pw, h=page.ph, location=loc, useOpsz=useOpsz, context=c)
        >>> style = dict(stroke=0, strokeWidth=0.25, leading=em(1.3), fontSize=48, xTextAlign=RIGHT)
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> #font2 = findFont('Upgrade-Regular')
        >>> #font2 = findFont('Escrow-Bold')
        >>> gs = Waterfall(font2, parent=page, conditions=conditions, style=style, w=page.pw, h=page.ph, padding=20, location=loc, useOpsz=useOpsz, context=c)
        >>> #score = doc.solve()
        >>> doc.export('_export/%sWaterfall_opsz_%s.pdf' % (font1.info.familyName, useOpsz))

        TODO: Make self.css('xTextAlign') work for CENTER
        """
        TextBox.__init__(self, **kwargs)
        c = self.context
        self.useOpsz = useOpsz # Only for the sample lines. Labels always have opsz.
        self.f = f
        if not location:
            location = {}
        self.factor = factor # Decreasing multiplication factor for fontSize
        style = self.style.copy()
        labelStyle = self.style.copy()
        labelStyle['font'] = self.getInstance(f, dict(opsz=labelSize)).path
        labelStyle['fontSize'] = labelSize
        labelStyle['leading'] = em(1)

        w = self.pw # Initial with to fit top sample
        location['opsz'] = None
        style['font'] = self.getInstance(self.f, self.getLocation(self.f, location)).path
        sampleText = sampleText or self.SAMPLE
        matchingLine = c.newString(sampleText+'\n', style=style, w=w)
        style['fontSize'] = fontSize = pt(int(matchingLine.fittingFontSize / 8)) * 8

        bs = c.newString('', style=style)
        while fontSize >= 12:
            # Still fitting? Otherwise stop the loop
            # TODO: Measure both lines (label + samleText) for fitting.
            tw, th = bs.size
            if th > self.ph:
                break
            # Make the optional label
            if showLabel:
                label = '%s %spt | opsz = %s\n' % (self.f.info.familyName, asFormatted(fontSize, '%0.1f'), self.useOpsz)
                bs += c.newString(label, style=labelStyle)
            style['fontSize'] = fontSize = int(round(fontSize * self.factor))
            location['opsz'] = {True: fontSize, False: None}[self.useOpsz]
            style['font'] = self.getInstance(self.f, self.getLocation(self.f, location)).path
            bs += c.newString(sampleText+'\n', style=style)

        self.bs = bs

    def getAxisValue(self, vf, tag, value):
        """Answers the scaled value for the "tag" axis, where value (-1..0..1) is upscaled to
        ratio in (minValue, defaultValue, maxValue)."""
        if not tag in vf.axes:
            return None
        minValue, defaultValue, maxValue = vf.axes[tag]
        if not value:
            return defaultValue
        if value < 0: # Realative scale between minValue and default
            return defaultValue + (defaultValue - minValue)*value
        # else wdth > 0:  Relative scale between default and maxValue
        return defaultValue + (maxValue - defaultValue)*value

    def getLocation(self, vf, location):
        """Answers the instance of self, corresponding to the normalized location.
        (-1, 0, 1) values for axes [wght] and [wdth].
        The optical size [opsz] is supposed to contain the font size, so it is not normalized.
        If [opsz] is not defined, then set it to default, if the axis exist.
        """
        if not vf.axes:
            return {}
        if location is None:
            location = {}

        # Get real axis values.
        wght = self.getAxisValue(vf, 'wght', location.get('wght'))
        wdth = self.getAxisValue(vf, 'wdth', location.get('wdth'))
        opsz = location.get('opsz')

        if not opsz and 'opsz' in vf.axes:
            opsz = vf.axes['opsz'][1] # Use default value

        # Make location dictionary
        return dict(wght=wght, wdth=wdth, opsz=opsz)

    def getInstance(self, vf, location):
        """Return the instance font at this location. The font is stored as file,
        # so it correspondents to normal instance.path behavior."""
        if vf.axes:
            return getVarFontInstance(vf, location)
        return vf


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
