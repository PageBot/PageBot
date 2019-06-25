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
#     glyphset.py
#
from pagebot.toolbox.units import pointOffset
from pagebot.elements.variablefonts.basefontshow import BaseFontShow
from pagebot.toolbox.future import chr

class GlyphSet(BaseFontShow):
    """Showing the specified (variable) font as full page with a matrix
    of all glyphs in the font.

    """
    def __init__(self, f, **kwargs):
        """
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> from pagebot.toolbox.color import color, blackColor
        >>> from pagebot.toolbox.units import em
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> style = dict(gh=16, fill=color(0.95), leading=em(1.4), fontSize=24)
        >>> conditions = [Fit()]
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF')
        >>> gs = GlyphSet(font1, parent=page, conditions=conditions, padding=40, style=style, context=c)
        >>> style = dict(stroke=blackColor, strokeWidth=0.25, gh=8, leading=em(1.4), fontSize=18) # Smaller fontSize and grid.
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> #font2 = findFont('Upgrade-Regular')
        >>> #font2 = findFont('Escrow-Bold')
        >>> gs = GlyphSet(font2, parent=page, conditions=conditions, style=style, padding=40, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sGlyphSet.pdf' % font1.info.familyName)
        """
        BaseFontShow.__init__(self, **kwargs)
        self.f = f # (Variable) font instance


    def build(self, view, origin, drawElements=True, **kwargs):
        """Default drawing method just drawing the frame.
        Probably will be redefined by inheriting element classes."""
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        self.buildFrame(view, p) # Draw optional frame or borders.

        # Let the view draw frame info for debugging, in case view.showFrame == True
        view.drawElementFrame(self, p)

        if self.drawBefore is not None: # Call if defined
            self.drawBefore(self, view, p)

        self.drawMatrix(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'


    def drawMatrix(self, view, origin, **kwargs):
        """Draw the matrix of available glyphs in the font, in font.cmap order and
        starting at the first sorted glyph after the space.

        TODO
        Check for overflow on multiple pages
        Optional to iterate over the font size until all glyphs fit (grow and shrink)
        Add optional filtering by glyph set or unicode range or filter function or regular expression
        Make self.COLS and self.ROWS respond to the request font size.
        Add optional showing of name and/or unicode
        Show Variable Fonts by location
        Show relations by features and/or GSUB substitution.
        Show in Fontographer or Ikarus layout for legacy fun.
        """
        c = self.context
        ox, oy, _ = origin
        fontSize = self.css('fontSize')
        cw = fontSize*1.6 # TODO: This should be optional as style attribute
        x = 0
        y = self.h - self.pt - cw
        for u, glyphName in sorted(self.f.cmap.items()):
            if u <= 32: # Skip any control characters and space
                continue
            bs = c.newString(chr(u), style=dict(font=self.f.path, fontSize=fontSize))
            tw, th = bs.size
            c.text(bs, (ox+x+self.pl-tw/2, oy+y))
            x += cw
            if x >= self.pw:
                x = 0
                y -= cw
            if y < 0:
                break

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
