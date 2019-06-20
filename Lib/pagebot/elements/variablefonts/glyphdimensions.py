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
#     glyphdimensions.py
#
from pagebot.toolbox.units import pointOffset
from pagebot.elements.variablefonts.basefontshow import BaseFontShow

class GlyphDimensions(BaseFontShow):
    """Showing the specified (variable) font large glyphs with a variety
    of optional measures and indicator.

    """
    def __init__(self, f, glyphName=None, **kwargs):

        """

        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> from pagebot.toolbox.units import em
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> style = dict(gh=16, fill=0.95, leading=em(1.4), fontSize=24)
        >>> conditions = [Fit()]
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF', lazy=False)
        >>> gs = GlyphDimensions(font1, parent=page, conditions=conditions, glyphName='S', padding=40, style=style, context=c)
        >>> style = dict(stroke=0, strokeWidth=0.25, gh=8, leading=em(1.4), fontSize=18) # Smaller fontSize and grid.
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> #font2 = findFont('Upgrade-Regular')
        >>> #font2 = findFont('Escrow-Bold')
        >>> gs = GlyphDimensions(font2, parent=page, conditions=conditions, glyphName='Q', style=style, padding=40, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sGlyphDimensions.pdf' % font1.info.familyName)

        >>> from pagebot.fonttoolbox.objects.font import Font
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('RobotoDelta-VF')
        >>> location = dict(SHPE=360, wght=500)
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=1, context=c)
        >>> style = dict(gh=16, fill=0.95, leading=em(1.4), fontSize=24)
        >>> conditions = [Fit()]
        >>> page = doc[1]
        >>> instance = font.getInstance(location=location)
        >>> gs = GlyphDimensions(instance, parent=page, glyphName='H', conditions=conditions, padding=40, style=style, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sGlyphDimensions.pdf' % font.info.familyName)
        """
        BaseFontShow.__init__(self, **kwargs)
        self.f = f # Font instance
        self.glyphName = glyphName or 'H'

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

        self.drawGlyphDimensions(view, p, **kwargs)

        if self.drawAfter is not None: # Call if defined
            self.drawAfter(self, view, p)

        self._restoreScale(view)
        view.drawElementInfo(self, origin) # Depends on flag 'view.showElementInfo'


    def drawGlyphDimensions(self, view, origin, **kwargs):
        """Draw the the indicated glyph(s), with dimensions and other indicator.
        """
        c = self.context
        ox, oy, _ = origin

        for fontSize in (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20):
            glyph = self.f[self.glyphName]
            c.save()
            c.stroke(0, 0.25)
            c.fill((0.7, 0.7, 0.7, 0.6))
            # FIXME: no self.pw
            #s = (self.pw/glyph.width)
            #c.scale(s)
            c.drawPath(c.getGlyphPath(glyph), ((ox+self.pl), (oy+self.ph/3)))
            c.restore()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
