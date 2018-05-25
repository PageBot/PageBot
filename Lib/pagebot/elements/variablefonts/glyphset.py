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
from pagebot.elements import Element
from pagebot.toolbox.transformer import pointOffset

class GlyphSet(Element): 
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
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> m = 80
        >>> doc = Document(w=w, h=h, padding=30, originTop=False, context=c)
        >>> page = doc[1]
        >>> font = findFont('RobotoDelta-VF')
        >>> #font = findFont('AmstelvarAlpha-VF')
        >>> gs = GlyphSet(font, x=m, y=m, w=w-2*m, h=h-2*m, parent=page, context=c)
        >>> doc.export('_export/%sGlyphSet.pdf' % font.info.familyName)
        """
        Element.__init__(self, **kwargs)
        c = self.context
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


    def drawMatrix(self, view, p):
        c = self.context
        x, y, _ = p
        mx = 0
        my = self.h
        for u, glyphName in sorted(self.f.cmap.items()):
            if u <= 20: # Skip any control characters and space 
                continue
            bs = c.newString(unichr(u), style=dict(font=self.f.path, fontSize=self.FONTSIZE))
            c.text(bs, (x+mx, y+my-self.ROWS))
            mx += self.COLS
            if mx >= self.w:
                mx = 0
                my -= self.ROWS
            if my < 0:
                break


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
