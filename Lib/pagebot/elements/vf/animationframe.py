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
#     animationframe.py
#


from math import sin, cos, radians
from pagebot.elements import Rect
from pagebot.toolbox.units import pointOffset, pt
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.color import color

class AnimationFrame(Rect):
    """Showing one frame of an animation, supporting different states of a VariableFont

    """
    SAMPLE = 'Sample'

    def __init__(self, s, font, frames, frameIndex, phases=None, **kwargs):
        """
        >>> from random import random
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter, RIGHT
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> from pagebot.toolbox.units import em
        >>> c = DrawBotContext()
        >>> w, h = 2040, 1020 # Type Network banners
        >>> duration = 3 # Seconds
        >>> framesPerSecond = 10
        >>> frames = duration * framesPerSecond
        >>> doc = Document(w=w, h=h, padding=10, originTop=False, glyphName='Agrave', frameDuration=1/framesPerSecond, autoPages=frames, context=c)
        >>> font = findFont('RobotoDelta-VF')
        >>> sample = 'PageBot'
        >>> for pn in range(1, frames+1):
        ...     page = doc[pn]
        ...     style = dict(leading=em(1.4), fontSize=400, xTextAlign=RIGHT, fill=color(0))
        ...     gs = AnimationFrame(sample, font, frames, pn, parent=page, padding=20, style=style, w=page.pw, h=page.ph, context=c)
        >>> doc.export('_export/%sAnimation.gif' % font.info.familyName)

        TODO: Make self.css('xTextAlign') work for CENTER
        """
        Rect.__init__(self, **kwargs)
        self.vfFont = font
        self.frames = frames # Total amount of expected frames in the animation part
        self.frameIndex = frameIndex
        self.sampleText = s or self.SAMPLE
        self.phases = phases or {} # Dictionary for phasing values depending on frame index.

    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        c = self.context
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional background fill, frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        view.drawElementFrame(self, p)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # Draw that actual content of the element by stacked specimen rectangles.
        self.drawAnimatedFrame(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def drawAnimatedFrame(self, view, origin, **kwargs):
        """Draw the content of the element, responding to size, styles, font and content.
        Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
        if the axis exists.

        """
        wdthMin, wdthDefault, wdthMax = self.vfFont.axes['wdth']
        wghtMin, wghtDefault, wghtMax = self.vfFont.axes['wght']

        ox, oy, _ = origin
        c = self.context
        style = self.style.copy()
        #location = getScaledLocation(self.f, dict(wght=self.frameIndex/self.frames))
        #instance = getInstance(self.vfFont, location)
        phisin = sin(radians(self.frameIndex/self.frames * 360))
        phicos = cos(radians(self.frameIndex/self.frames * 360))

        style['textFill'] = color(1-phicos*0.3+0.5)
        # TODO: Not the right instance-weight is shown in export.
        wdthRange = wdthMax - wdthMin
        wghtRange = wghtMax - wghtMin
        location = dict(wdth=phisin*wdthRange/2+wdthRange/2+wdthMin, wght=phisin*wghtRange/2+wghtRange/2+wghtMin)
        instance = self.vfFont.getInstance(location)#instance.path
        style['font'] = instance.path
        #print(self.frameIndex, style['font'])
        #style['fontSize'] = self.h/3
        bs = c.newString(self.sampleText, style=style)
        tw, th = bs.size
        c.text(bs, (self.w/2 - tw/2, self.h/2))
        glyph = instance['ampersand']
        c.save()
        c.stroke(color(0), pt(0.25))
        gray = phisin*0.3+0.5
        c.fill(color(gray, gray, 1-gray, 0.6))
        s = 0.4
        c.scale(s)
        c.drawPath(c.getGlyphPath(glyph), ((ox+self.pl)/s, (oy+self.ph/4)/s))
        c.restore()

        # FIXME: should get local path using findFont(), but axis seem to be specific to
        # Bitcount.
        #path = "/Users/petr/Desktop/TYPETR-git/TYPETR-Bitcount-Var/variable_ttf/BitcountTest_DoubleCircleSquare4-VF.ttf"
        #f = Font(path)
        f = findFont('RobotoDelta-VF')

        if 'SHPE' in f.axes:
            SHPEMin, SHPEDefault, SHPEMax = f.axes['SHPE']
            SHPERange = SHPEMax - SHPEMin
            wghtMin, wghtDefault, wghtMax = self.vfFont.axes['wght']
            wghtRange = wghtMax - wghtMin
            location = dict(SHPE=phisin*SHPERange/2+SHPERange/2+SHPEMin, wght=phicos*wghtRange/2+wghtRange/2+wghtMin)
            instance = f.getInstance(location)#instance.path
            glyph = instance['A']

        """
        path = "/Users/petr/Desktop/TYPETR-git/TYPETR-Bitcount-Var/variable_ttf/BitcountTest_DoubleCircleSquare2-VF.ttf"
        f = Font(path)
        SHPEMin, SHPEDefault, SHPEMax = f.axes['SHPE']
        SHPERange = SHPEMax - SHPEMin
        wghtMin, wghtDefault, wghtMax = self.vfFont.axes['wght']
        wghtRange = wghtMax - wghtMin
        location = dict(SHPE=phisin*SHPERange/2+SHPERange/2+SHPEMin, wght=phicos*wghtRange/2+wghtRange/2+wghtMin)
        instance = f.getInstance(location)#instance.path
        glyph = instance['A']
        """
        c.save()
        c.stroke(color(1, 0, 0), pt(0.25))
        gray = phisin*0.3+0.7
        c.fill(color(gray, gray, gray, 0.8))
        s = 1
        c.scale(s)
        c.drawPath(c.getGlyphPath(glyph), ((ox+self.w/2+self.pl)/s, (oy+self.ph/4)/s))
        c.restore()


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
