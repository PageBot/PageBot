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
#     glyphset.py
#
from pagebot.toolbox.transformer import pointOffset
from pagebot.elements.variablefonts.basefontshow import BaseFontShow

class GlyphSet(BaseFontShow): 
    u"""Showing the specified (variable) font as full page with a matrix
    of all glyphs in the font.

    """
    COLS = 28
    ROWS = 28
    GUTTER = 12
    FONTSIZE = 24

    def __init__(self, f, **kwargs):
        u"""   
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> style = dict(gh=16, fill=0.95, rLeading=1.4)
        >>> conditions = [Fit()]
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF')
        >>> gs = GlyphSet(font1, parent=page, conditions=conditions, padding=40, style=style, context=c)
        >>> style = dict(stroke=0, strokeWidth=0.25, gh=8, rLeading=1.4)
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> #font2 = findFont('Upgrade-Regular')
        >>> #font2 = findFont('Escrow-Bold')
        >>> gs = GlyphSet(font2, parent=page, conditions=conditions, style=style, padding=40, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sGlyphSet.pdf' % font1.info.familyName)
        """
        BaseFontShow.__init__(self, **kwargs)
        self.f = f # Font instance


    def build(self, view, origin, drawElements=True):
        u"""Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.oPoint, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showElementFrame == True
        view.drawElementFrame(self, p) 

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        self.drawMatrix(view, p)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementMetaInfo(self, origin) # Depends on flag 'view.showElementInfo'


    def drawMatrix(self, view, origin):
        c = self.context
        ox, oy, _ = origin
        x = 0
        y = self.h - self.pt - self.COLS
        for u, glyphName in sorted(self.f.cmap.items()):
            if u <= 32: # Skip any control characters and space 
                continue
            bs = c.newString(unichr(u), style=dict(font=self.f.path, fontSize=self.FONTSIZE))
            tw, th = bs.textSize()
            c.text(bs, (ox+x+self.pl-tw/2, oy+y))
            x += self.COLS
            if x >= self.pw:
                x = 0
                y -= self.ROWS
            if y < 0:
                break


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
