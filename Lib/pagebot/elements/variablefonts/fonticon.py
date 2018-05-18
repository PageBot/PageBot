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
#	  fonticon.py
#
#     Draw the icon with optional information of the included font.
#

class FontIcon(Element):
    W = 30
    H = 40
    L = 2
    E = 8
    LABEL_RTRACKING = 0.02
    LABEL_RLEADING = 1.3

    def __init__(self, f, name=None, label=None, title=None, eId=None, c='F', s=1, line=None,
            labelFont=None, titleFont=None, x=0, y=0, show=True):
        self.f = f # Font instance
        self.labelFont = labelFont or f
        self.titleFont = titleFont, labelFont or f
        self.title = title
        self.name = name # Name below the icon
        self.label = label # Optiona second label line
        self.c = c # Character(s) in the icon.
        self.scale = s
        self.line = line or self.L
        self.x = x
        self.y = y
        self.show = show
        self.eId = eId

    def _get_w(self):
        return self.W*self.scale
    w = property(_get_w)

    def _get_ih(self):
        u"""Answer scaled height of the plain icon without name label."""
        return self.H*self.scale
    ih = property(_get_ih)

    def _get_h(self):
        h = self.ih
        if self.name:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        if self.label:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        if self.title:
            h += self.E*self.scale*1.4 # Extra vertical space to show the name.
        return h
    h = property(_get_h)

    def draw(self, orgX, orgY):
        if not self.show:
            return
        w = self.w # Width of the icon
        h = self.ih # Height of the icon
        e = self.E*self.scale # Ear size
        l = self.L*self.scale # Line
        x = self.x + orgX
        y = self.y + orgY

        c.newPath()
        c.moveTo((0, 0))
        c.lineTo((0, h))
        c.lineTo((w-e, h))
        c.lineTo((w, h-e))
        c.lineTo((w, 0))
        c.lineTo((0, 0))
        c.closePath()
        c.moveTo((w-e, h))
        c.lineTo((w-e, h-e))
        c.lineTo((w, h-e))

        c.save()
        c.fill(1)
        c.stroke(0, self.line)
        c.translate(x, y)
        c.drawPath()
        labelSize = e
        bs = c.newString(self.c,
                               style=dict(font=self.f.path,
                                          textFill=0,
                                          fontSize=h*2/3))
        tw, th = bs.textSize()
        c.text(bs, (w/2-tw/2, h/2-th/3.2))

        if self.title:
            bs = c.newString(self.title,
                                   style=dict(font=self.labelFont.path,
                                              textFill=0,
                                              rTracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.textSize()
            c.text(bs, (w/2-tw/2, self.ih+th/2))

        y = -self.LABEL_RLEADING*labelSize
        if self.name:
            bs = c.newString(self.name,
                                   style=dict(font=self.labelFont.path,
                                              textFill=0,
                                              rTracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.textSize()
            c.text(bs, (w/2-tw/2, y))
            y -= self.LABEL_RLEADING*labelSize
        if self.label:
            bs = c.newString(self.label,
                                   style=dict(font=self.labelFont.path,
                                              textFill=0,
                                              rTracking=self.LABEL_RTRACKING,
                                              fontSize=labelSize))
            tw, th = bs.textSize()
            c.text(bs, (w/2-tw/2, y))
        c.restore()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
