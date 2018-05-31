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
#     animationframe.py
#
from __future__ import division # Make integer division result in float.

from pagebot.elements import Rect
from pagebot.toolbox.transformer import pointOffset
from pagebot.fonttoolbox.objects.font import getInstance

class AnimationFrame(Rect):
    u"""Showing one frame of an animation, supporting different states of a VariableFont 

    """
    SAMPLE = 'Sample'

    def __init__(self, f, frames, frameIndex, sampleText=None, **kwargs):
        u"""
        >>> from random import random
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter, RIGHT
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> c = DrawBotContext()
        >>> w, h = 2040, 1020 # Type Network banners
        >>> duration = 3 # Seconds
        >>> framesPerSecond = 10
        >>> frames = duration * framesPerSecond
        >>> doc = Document(w=w, h=h, padding=10, originTop=False, frameDuration=1/framesPerSecond, autoPages=frames, context=c)
        >>> font = findFont('AmstelvarAlpha-VF')
        >>> for pn in range(1, frames+1):
        ...     page = doc[pn]
        ...     style = dict(rLeading=1.4, fontSize=48, xTextAlign=RIGHT)
        ...     gs = AnimationFrame(font, frames, pn, parent=page, padding=20, style=style, w=page.pw, h=page.ph, context=c)
        >>> doc.export('_export/%sAnimation.gif' % font.info.familyName)

        TODO: Make self.css('xTextAlign') work for CENTER
        """
        Rect.__init__(self, **kwargs)
        self.f = f
        self.frames = frames # Total amount of expected frames in the animation part
        self.frameIndex = frameIndex
        self.sampleText = sampleText or self.SAMPLE

    def build(self, view, origin, drawElements=True):
        u"""Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        c = self.context
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)
        p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional background fill, frame or borders.

        # Let the view draw frame info for debugging, in case view.showElementFrame == True
        view.drawElementFrame(self, p) 

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        # Draw that actual content of the element by stacked specimen rectangles.
        self.drawAnimatedFrame(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on flag 'view.showElementInfo'

    def drawAnimatedFrame(self, view, origin):
        u"""Draw the content of the element, responding to size, styles, font and content.
        Create 2 columns for the self.fontSizes ranges that show the text with and without [opsz]
        if the axis exists.

        """
        ox, oy, _ = origin
        c = self.context
        style = self.style.copy()
        #location = getScaledLocation(self.f, dict(wght=self.frameIndex/self.frames))
        #instance = getInstance(self.f, location)
        style['textFill'] = 1/self.frames * self.frameIndex
        # TODO: Not the right instance-weight is shown in export.
        instance = getInstance(self.f, dict(wdth=self.frameIndex/self.frames*(600-100)+100, wght=self.frameIndex/self.frames*(900-200)+200))#instance.path
        style['font'] = instance.path
        #print(self.frameIndex, style['font'])
        style['fontSize'] = self.h/2
        bs = c.newString(self.sampleText, style=style)
        tw, th = bs.textSize()
        c.text(bs, (self.w/2 - tw/2, self.h/2))

        glyph = instance['H']
        c.save()
        c.stroke(0, 0.25)
        c.fill((0.7, 0.7, 0.7, 0.6))
        s = 0.45
        c.scale(s)
        c.drawPath(glyph.path, ((ox+self.pl)/s, (oy+self.ph/3)/s))
        c.restore()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
