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
#     books/photobook/titlepage.py
#
from pagebot.conditions import Center2Center, Bottom2Bottom, Fit2Width, Top2Top
#from pagebot.elements import newTextBox # gives cyclic import error.
from pagebot.elements.pbtextbox import TextBox

def makeTitlePage(page, title=None, text=None):
    """Cover template for photo books."""
    if title is not None:
        tw, th = title.size
        TextBox(title, parent=page, h=th, conditions=[Fit2Width(), Top2Top()])
    if text is not None:
        tw, th = text.size
        TextBox(text, parent=page, w=page.pw, h=th, stroke=(0, 1, 0), 
            conditions=[Center2Center(), Bottom2Bottom()])
