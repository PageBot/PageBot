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
#     sampler.py
#


from pagebot.elements import TextBox

class Sampler(TextBox):
    """Showing the specified (variable) font as full page with a samples of glyphs.

    """
    SAMPLE = 'Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz\n1234567890\n!@#$%&'

    def __init__(self, f, sampleText=None, **kwargs):
        """
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> from pagebot.document import Document
        >>> from pagebot.constants import Letter, RIGHT
        >>> from pagebot.contexts.drawbotcontext import DrawBotContext
        >>> from pagebot.conditions import *
        >>> from pagebot.toolbox.units import em
        >>> from pagebot.toolbox.color import color
        >>> c = DrawBotContext()
        >>> w, h = Letter
        >>> doc = Document(w=w, h=h, padding=80, originTop=False, autoPages=2, context=c)
        >>> style = dict(fill=color(0.95), leading=em(1.4), fontSize=48, xTextAlign=RIGHT)
        >>> conditions = [Fit()] # FIX: Does not seem to work for TextBox
        >>> page = doc[1]
        >>> font1 = findFont('AmstelvarAlpha-VF')
        >>> gs = Sampler(font1, parent=page, conditions=conditions, padding=20, style=style, w=page.pw, h=page.ph, context=c)
        >>> style = dict(stroke=0, strokeWidth=0.25, leading=em(1.4), fontSize=48, xTextAlign=RIGHT)
        >>> page = doc[2]
        >>> font2 = findFont('RobotoDelta-VF')
        >>> #font2 = findFont('Upgrade-Regular')
        >>> #font2 = findFont('Escrow-Bold')
        >>> gs = Sampler(font2, parent=page, conditions=conditions, style=style, w=page.pw, h=page.ph, padding=20, context=c)
        >>> score = doc.solve()
        >>> doc.export('_export/%sSampler.pdf' % font1.info.familyName)

        TODO: Make self.css('xTextAlign') work for CENTER
        """
        TextBox.__init__(self, **kwargs)
        c = self.context
        style = self.style.copy()
        style['font'] = f.path
        sampleText = c.newString(sampleText or self.SAMPLE, style=style)
        self.bs = sampleText
        self.f = f # Save font instance for later usage.

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
