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
#     calendar/photocalendar/coverpage.py
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
        tw, _ = title.size
        newTextBox(title, parent=page, w=tw, conditions=[Center2Center(), Bottom2Top()])
    if author is not None:
        tw, _ = author.size
        newTextBox(author, parent=page, w=tw, stroke=(0, 1, 0), conditions=[Center2Center(), Top2Bottom()])
    page.solve()
