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
#     books/photobook/cover.py
#
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.constants import *

def makeCoverPage(page, imagePath=None, title=None, author=None, fill=None):
    """Cover template for photo books.
    """
    if fill is not None:
    	newRect(fill=fill, parent=page, conditions=[Fit2Bleed()])
    if imagePath is not None:
    	newImage(imagePath, x=page.pl, y=page.pb, w=page.pw, h=page.ph, parent=page)
    if title is not None:
    	tw, th = title.size
    	newTextBox(title, parent=page, w=tw, h=th, stroke=(0, 0, 1), conditions=[Center2Center(), Top2TopSide()])
    if author is not None:
    	tw, th = author.size
    	dd = newTextBox(author, parent=page, w=tw, h=th, stroke=(0, 1, 0), conditions=[Center2Center(), Top2Bottom()])
    print(dd.top, page.pb, dd.y, dd.h, dd.y+dd.h, dd.bottom, dd.isTopOnBottom())
    page.solve()
    print(dd.top)
