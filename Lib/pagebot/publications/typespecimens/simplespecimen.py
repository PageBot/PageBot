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
#     simplespecimens.py
#
from pagebot.publications.typespecimens.basetypespecimen import BaseTypeSpecimen
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.fonttoolbox.objects.font import findFont

class SimpleSpecimen(BaseTypeSpecimen):


    def newSampleDocument(self, autoPages=None, theme=None, **kwargs):

        if theme is None:
            theme = self.theme
        c = theme.mood.light1
        f = findFont('PageBot-Regular')

        doc = self.newDocument(autoPages=autoPages or 1, **kwargs)
        page = doc[1]
        bs = None
        for n in range(8, 48):
            style = dict(font=f, fontSize=n, leading=n*1.1)
            bs1 = self.context.newString('ABCDEFGHIJKLMNOPQRSTUVWXYZ\n', style=style)
            tw1, th1 = bs1.size
            if bs is None:
                bs = bs1
            tw, th = bs.size
            if max(tw, tw1) > page.pw or (th + th1) > page.ph:
                break
            bs += bs1

        newTextBox(bs, parent=page, fill=c, h=th, conditions=[Left2Left(), Fit2Width(), Top2Top()])
        page.solve()
        return doc

   