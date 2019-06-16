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
#     typespecimens.py
#
from pagebot.publications.typespecimens.basetypespecimen import BaseTypeSpecimen
from pagebot.elements import *
from pagebot.conditions import *

class TypeSpecimen(BaseTypeSpecimen):
    

    def newSampleDocument(self, autoPages=None, theme=None, **kwargs):

        if theme is None:
            theme = self.theme
        c = theme.mood.base1

        doc = self.newDocument(autoPages=autoPages or 1, **kwargs)
        page = doc[1]
        newRect(parent=page, fill=c)
        return doc

  