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
#     books/photobook/titlepage.py
#
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.constants import *

def makeTitlePage(page, title=None, text=None):
    """Cover template for photo books.
    """
    if title is not None:
        tw, th = title.size
        newTextBox(title, parent=page, h=th, conditions=[Fit2Width(), Top2Top()])
    if text is not None:
        tw, th = text.size
        newTextBox(text, parent=page, w=page.pw, h=th, stroke=(0, 1, 0), 
            conditions=[Center2Center(), Bottom2Bottom()])
