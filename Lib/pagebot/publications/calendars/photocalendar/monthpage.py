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
#     calendars/photocalendar/monthpage.py
#
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.constants import *
from pagebot.toolbox.dating import Dating, now

def makeMonthPage(page, month, year=None):
    """Cover template for photo books.
    """
    if year is None:
    	year = now().year
    d = Dating(year=year, month=month)
    print(d, d.week, (d+7).week)
    newTextBox(month, parent=page, fill=0.5, conditions=[Left2Left(), Top2Top(), Fit2Width(), Fit2Bottom()])
